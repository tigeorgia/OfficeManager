from django.shortcuts import render
from employee.views import checkuserloggedin
from leaverequest.models import LeaveForm, Leave
from django.utils.datetime_safe import datetime
from publicholidays.models import PublicHoliday
from datetime import timedelta
from timesheet.tshelpers import send_notification, months
from decimal import Decimal
from timesheet.models import TimeSheet



@checkuserloggedin
def request_leave( request, employee ):

    message = ''


    if request.method == "POST":
        leave_form = LeaveForm( request.POST )

        if leave_form.is_valid():

            start_date = datetime.strptime( request.POST["start_date"], '%Y-%m-%d' )

            end_date = None
            if request.POST["end_date"] != '':
                end_date = datetime.strptime( request.POST["end_date"], '%Y-%m-%d' )

            start_hour = None
            if request.POST["start_hour"] != '':
                start_hour = datetime.strptime( request.POST["start_hour"], '%H:%M' )

            end_hour = None
            if request.POST["end_hour"] != '':
                end_hour = datetime.strptime( request.POST["end_hour"], '%H:%M' )


            if start_hour is not None and end_hour is not None:
                end_date = start_date


            leave_request = Leave( 
                                  start_date = start_date,
                                  end_date = end_date,
                                  start_hour = start_hour,
                                  end_hour = end_hour,
                                  employee = employee,
                                  type = request.POST["type"],
                                  comment = request.POST["comment"],
                                  submit_date = datetime.today(),
                                  approved_by = employee.supervisor.first_name + ' ' + employee.supervisor.last_name,
                                  workdays_requested = 0,
                                  sick_balance = employee.leave_balance_SICK,
                                  vacation_balance = employee.leave_balance_HOLS
                                  )

            request_status = check_if_can_be_submitted( leave_request)
            if request_status[0] == True:


                working_days = count_working_days( leave_request )
                leave_request.workdays_requested = working_days


                if request.POST['button'] == "Submit":
                    message = "%s Leave request for %.2f working days has been submitted for approval." % ( 
                                                                                                        dict( leave_request.TYPES )[ leave_request.type],
                                                                                                        working_days,
                                                                                                        )
                else:
                    message = '%s Leave request for %.2f working days.' % ( 
                                                                        dict( leave_request.TYPES )[ leave_request.type],
                                                                        working_days,
                                                                        )


                hols_result = employee.leave_balance_HOLS
                if leave_request.type == 'HOLS':
                    hols_result -= working_days


                sick_result = employee.leave_balance_SICK
                if leave_request.type == 'SICK':
                    sick_result -= working_days



                message += '\nFollowing approval your resulting balance will be\nVacation: %.2f, Sick %.2f' % ( hols_result, sick_result )

                if request.POST['button'] == "Submit":
                    leave_request.save()

                    send_notification( request, "SUBMITTED", leave_request )

                    leave_form = LeaveForm()
                else:
                    leave_form = LeaveForm( request.POST )

            else:
                message = "This request can't be submitted because\nyour time sheet for %s\nalready exists in the system" % request_status[1]

    else:
        leave_form = LeaveForm()


    return render( request, "request_leave.html", {
                                                   "employee": employee,
                                                   "form": leave_form,
                                                   "message": message,
                                                   } )

# will say false if it spans already submitted timesheet
def check_if_can_be_submitted( leave_request):
    
    start_date = leave_request.start_date
    start_period = "%s %d" % ( months[ start_date.month - 1], start_date.year)
    
    time_sheet = TimeSheet.objects.filter( employee = leave_request.employee, period = start_period)
    
    if time_sheet:
        return ( False, start_period) 
    
    end_date = leave_request.end_date
    end_period = "%s %d" % ( months[ start_date.month - 1], end_date.year)
    
    time_sheet = TimeSheet.objects.filter( employee = leave_request.employee, period = end_period)
    
    if time_sheet:
        return ( False, end_period) 

    
    return ( True, [] )



def count_working_days( leave_request ):
    start_date = leave_request.start_date
    end_date = leave_request.end_date


    holidays = PublicHoliday.objects.filter( date__gte = start_date
                                             ).filter( date__lte = end_date )

    holiday_count = 0

    for holiday in holidays:
        if holiday.date.weekday() < 5 and holiday.type == "Public holiday":
            holiday_count += 1

    current_date = start_date

    if leave_request.start_date != leave_request.end_date:
        workday_count = 0
        while True:
            if current_date.weekday() < 5:
                workday_count += 1

            if current_date == end_date:
                break

            current_date += timedelta( days = 1 )


        workday_count -= holiday_count

    else:
        start_hour = datetime( 
                              leave_request.start_date.year,
                              leave_request.start_date.month,
                              leave_request.start_date.day,
                              leave_request.start_hour.hour,
                              leave_request.start_hour.minute,
                              )

        end_hour = datetime( 
                              leave_request.start_date.year,
                              leave_request.start_date.month,
                              leave_request.start_date.day,
                              leave_request.end_hour.hour,
                              leave_request.end_hour.minute,
                              )


        diff = end_hour - start_hour

        days = ( float( diff.seconds ) / 3600. ) / 8.
        workday_count = days


    return Decimal( workday_count )

