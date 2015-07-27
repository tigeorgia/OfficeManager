# collects the data for timesheet_submition
import datetime
from django.utils.translation import ugettext as _
from django.http.response import HttpResponse
from django.core.mail import send_mail
import thread
import timesheet
from timesheet.models import TimeSheet
from leaverequest.models import Leave, LeaveForm
from employee.models import Profile
from budgetshare.models import SalaryAssignment
from publicholidays.models import PublicHoliday
from decimal import Decimal


weekdays = ( _( 'Monday' ), _( 'Tuesday' ), _( 'Wednesday' ), _( 'Thursday' ), _( 'Friday' ), _( 'Saturday' ), _( 'Sunday' ) )
months = ( _( "January" ), _( "February" ), _( "March" ), _( "April" ), _( "May" ), _( "June" ),
           _( "July" ), _( "August" ), _( "September" ), _( "October" ), _( "November" ), _( "December" ) )

# identifies leave requests within a tuple of dates
def find_leave_requests( employee, dates ):


    # only leaves related to these dates and approved are used in the calculation
    leave_requests = Leave.objects.filter( employee = employee
                                           ).exclude( end_date__lte = dates[0]
                                                      ).exclude( start_date__gte = dates[1]
                                                                 ).exclude( approve_date = None )
    leave_days = {}
    for l_request in leave_requests:

        
        current_day = l_request.start_date
        while True:

            if current_day.month == dates[0].month:
                leave_days[current_day.day] = {}
                leave_days[current_day.day]['type'] = ( dict( l_request.TYPES )[l_request.type], l_request.type )
                if l_request.start_date == l_request.end_date:
                    start_dtime = datetime.datetime.combine(l_request.start_date, l_request.start_hour)
                    end_dtime = datetime.datetime.combine(l_request.start_date, l_request.end_hour)
                    
                    amount = end_dtime - start_dtime
                    
                    amount = amount.seconds / (8. * 3600) 
                    leave_days[current_day.day]['amount'] = amount
                else:
                    leave_days[current_day.day]['amount'] = 1

            if current_day == l_request.end_date:
                break

            current_day += datetime.timedelta( days = 1 )

    # the method (will) return(s) a dictionary with keys and day numbers and values as leave type
    return {'requests':leave_requests, 'days': leave_days}


def find_public_holidays( dates ):

    public_holidays = PublicHoliday.objects.filter( date__lte = dates[1] ).filter( date__gte = dates[0] )
    leave_days = {}

    for holiday in public_holidays:
        if holiday.type.lower() == 'public holiday':
            leave_days[ holiday.date.day] = holiday.name

    return {'holidays': public_holidays, 'days': leave_days}


def documents_to_approve( request ):
    supervised_employees = Profile.objects.filter( supervisor = request.user )

    time_sheets = TimeSheet.objects.filter( employee = supervised_employees, approve_date = None )
    leave_requets = Leave.objects.filter( employee = supervised_employees, approve_date = None, declined = False )

    return { 'time_sheets': time_sheets, 'leave_requests' : leave_requets }


def timesheet_salary_sources( employee, period ):

    assignments = SalaryAssignment.objects.filter( employee = employee, period = period )

    output = {}

    for s_assign in assignments:
        if s_assign.percentage == 0:
            continue

        output[ s_assign.source.code.upper()] = ( s_assign.percentage, s_assign.submitted_by )

    return output


def generate_timesheet_data( employee, period, time_sheet = None, recalc_balances = False ):

    start_hour, start_minute = employee.workday_start.hour, employee.workday_start.minute
    end_hour, end_minute = employee.workday_end.hour, employee.workday_end.minute

    working_time = end_hour * 60 + end_minute - start_hour * 60 - start_minute

    day_working_time = working_time / 60.  # - employee.break_hours


    working_time = "%.2f" % day_working_time



    # define dates
    if time_sheet is None:
        period_first_day = datetime.datetime.strptime( period, '%B %Y' )
        first_day = datetime.date( day = 1, month = period_first_day.month, year = period_first_day.year )

        last_day = first_day + datetime.timedelta( days = 32 )
        last_day = datetime.date( day = 1, month = last_day.month, year = last_day.year )

        last_day = last_day - datetime.timedelta( days = 1 )
    else:
        first_day, last_day = time_sheet.start_date, time_sheet.end_date


    # finding the leave requests
    leave_requests = find_leave_requests( employee, ( first_day, last_day ) )
    # calculate leave days and mark the in the list during generation
    # then we have to generate the leave form

    public_holidays = find_public_holidays( ( first_day, last_day ) )

    calendar = []

    current_day = first_day

    leave_used = {'HOLS':0, 'SICK':0}
    month_working_time = 0.
    while True:
        actual_working_time = working_time

        if current_day < employee.contract_start or current_day > employee.contract_end:
            actual_working_time = '0.00'



        not_working_time = 0
        weekday = current_day.weekday()
        if weekday > 4:
            calendar.append( ( current_day.day, weekdays[ weekday], '', '', '', '', weekday ) )
        else:
            if current_day.day in public_holidays['days'].keys():
                calendar.append( ( current_day.day,
                                   weekdays[ weekday],
                                   public_holidays['days'][current_day.day] ,
                                   public_holidays['days'][current_day.day] ,
                                   actual_working_time,
                                   weekday
                                    ) )
            elif current_day.day in leave_requests['days'].keys():

                # update balances
                if leave_used.has_key( leave_requests['days'][current_day.day]['type'][1] ):
                    leave_used[leave_requests['days'][current_day.day]['type'][1]] += leave_requests['days'][current_day.day]['amount']
                else:
                    not_working_time = day_working_time

                calendar.append( ( current_day.day,
                                   weekdays[ weekday],
                                   leave_requests['days'][current_day.day]['type'][0] ,
                                   leave_requests['days'][current_day.day]['type'][0] ,
                                   "%.2f" % ( max( float( actual_working_time ) - not_working_time, 0 ) ),
                                   weekday
                                    ) )


            else:
                calendar.append( ( current_day.day,
                                   weekdays[ weekday],
                                   "%02d:%02d" % ( employee.workday_start.hour, employee.workday_start.minute ) ,
                                   "%02d:%02d" % ( employee.workday_end.hour, employee.workday_end.minute ) ,
                                   actual_working_time,
                                   weekday
                                    ) )

            month_working_time += max( 0.0, float( actual_working_time ) - not_working_time )

        if current_day == last_day:
            break
        current_day = current_day + datetime.timedelta( days = 1 )


    report_period = period


    if time_sheet:
        leave_data = ( 
                      time_sheet.leave_balance_before_HOLS,
                      time_sheet.leave_balance_before_SICK,
                      time_sheet.leave_earn_HOLS,
                      time_sheet.leave_earn_SICK,
                      time_sheet.leave_used_HOLS,
                      time_sheet.leave_used_SICK,
                      time_sheet.leave_balance_HOLS,
                      time_sheet.leave_balance_SICK,
                      )
    else:
        # leave balances

        balance_HOLS = employee.leave_balance_HOLS# + Decimal( leave_used['HOLS'])

        balance_SICK = employee.leave_balance_SICK# + Decimal( leave_used['SICK'])

        earn_HOLS = employee.leave_earn_HOLS
        earn_SICK = employee.leave_earn_SICK
        used_HOLS = leave_used['HOLS']
        used_SICK = leave_used['SICK']

        end_HOLS = balance_HOLS - Decimal( leave_used['HOLS']) + employee.leave_earn_HOLS
        end_SICK = balance_SICK - Decimal( leave_used['SICK']) + employee.leave_earn_SICK


        leave_data = ( 
                      balance_HOLS,
                      balance_SICK,
                      earn_HOLS,
                      earn_SICK,
                      used_HOLS,
                      used_SICK,
                      end_HOLS,
                      end_SICK
                      )

    leave_data_str = []
    for idx in range( len( leave_data ) ):
        leave_data_str.append( "%.2f" % leave_data[idx] )


    if time_sheet:
        supervisor = time_sheet.approved_by
        approve_date = time_sheet.approve_date
    else:
        supervisor = ""
        approve_date = None

    s_source = timesheet_salary_sources( employee, report_period )

    result = {'calendar': calendar,
              'working_time': month_working_time,
              'period': report_period,
              'leave': leave_data_str,
              'leave_data':leave_data ,
              'dates': ( first_day, last_day ),
              'supervisor': supervisor,
              'salary_sources': s_source,
              'approve_date': approve_date}

    return result




def send_notification( request, notify_type, email_data ):
    # # OFF for development
    #     return

    # recipient - SUPERVISOR, MANAGER(s), EMPLOYEE
    # notify_type - SUBMITTED, APPROVED, SALARY_ASSIGNED
    # email_data - whatever it was that is the subject of message (time sheet, leave request, salary assignment)
    #    system will take information from it and compose a reasonable, informative email

    if notify_type == "SUBMITTED":
        # notify supervisor about documents to approve
        recipient = [email_data.employee.supervisor.email]
        subject = "New document to approve"


        sender = employee_name = "%s %s" % ( email_data.employee.user.first_name, email_data.employee.user.last_name )

        site_address = request.build_absolute_uri().split( '/' )
        site_address[-1] = 'docstoapprove'
        site_address = '/'.join( site_address )

        goto_content = "Please go to:\n\n%s\n\nto approve the document." % site_address

        if type( email_data ) == TimeSheet:

            info_content = "Employee: %s has submitted a time sheet for %s\n\n" % ( employee_name, email_data.period )

        if type( email_data ) == Leave:

            info_content = "Employee: %s has submitted a leave request\n\n" % ( employee_name, )

        content = info_content + goto_content


    if notify_type == "APPROVED":

        # notify employee about approval
        recipient = [email_data.employee.user.email]
        sender = "%s %s" % ( request.user.first_name, request.user.last_name )

        site_address = request.build_absolute_uri().split( '/' )
        site_address[-1] = 'approveddocuments'
        site_address = '/'.join( site_address )
        
        if type( email_data ) == Leave:

            subject = "Leave request approved"
            content = "Your leave request for dates %s - %s has been approved.\n\n" % ( email_data.start_date, email_data.end_date )
            content += "To print your document go to %s ." % site_address
            #             document = "leave request"

        if type( email_data ) == TimeSheet:

            subject = "Time sheet approved"
            content = "Your time sheet for %s has been approved.\n" % ( email_data.period )
            content += "To print your document go to:\n %s ." % site_address
            #             document = "time sheet"


        # notify managers about complete document

        # collect office manager emails
        #         managers = Profile.objects.filter( role = "OMAN" )
        #         email_list = []
        #         for manager in managers:
        #             email_list.append( manager.user.email )
        # 
        #         manager_subject = "New approved document"
        # 
        #         site_address = request.build_absolute_uri().split( '/' )
        #         site_address[-1] = 'approveddocuments'
        #         site_address = '/'.join( site_address )
        # 
        #         document_employee = "%s %s" % ( email_data.employee.user.first_name, email_data.employee.user.last_name )
        # 
        #         manager_content = "%s has approved a %s for %s \n\n" % ( sender, document, document_employee )
        #         manager_content += "Please go to:\n\n%s\n\nto view approved documents." % site_address
        # 
        #         recipient = email_list
        # 
        # 
        #         thread.start_new( send_mail, ( manager_subject, manager_content, sender, email_list, True ) )

        # send_mail( subject, content, sender, email_list, fail_silently = True )



    if notify_type == "SALARY_ASSIGNED":
        recipient = [email_data.employee.user.email]

        sender = "%s %s" % ( request.user.first_name, request.user.last_name )

        site_address = request.build_absolute_uri().split( '/' )
        site_address[-1] = 'submittimesheet'
        site_address = '/'.join( site_address )

        content = "Your salary assignment for %s is complete.\n\n" % email_data.period
        content += "Please go to \n\n%s\n\nto submit your time sheet for %s" % ( site_address, email_data.period )

        subject = "Submit your time sheet"

    thread.start_new( send_mail, ( subject, content, sender, recipient, True ) )

    # send_mail( subject, content, sender, recipient, fail_silently = True )



