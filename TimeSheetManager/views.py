from django.shortcuts import render
from django.contrib.auth import logout, login, authenticate
from TimeSheetManager import models
from TimeSheetManager.models import Employee, TimeSheet, Leave, SalarySourceForm, SalarySource, \
    SalaryAssignment
import ldap
from OfficeManager import settings
from django.views.decorators.csrf import csrf_exempt

from TimeSheetManager import timesheet
from django.contrib.auth.models import User
import datetime
from django_auth_ldap.backend import LDAPBackend
from TimeSheetManager.timesheet import send_notification






# a little ldap helper, need to change it so it gives me login names instead of display names
def available_user_list():
    ldap_client = ldap.initialize( settings.AUTH_LDAP_SERVER_URI )
    ldap_client.simple_bind_s( settings.AUTH_LDAP_BIND_DN, settings.AUTH_LDAP_BIND_PASSWORD )

    ldap_attrs = ['givenName', 'sn', 'sAMAccountName', 'mail']

    ldap_users = ldap_client.search_s( settings.ORG_LDAP_BASE_DN,
                                       ldap.SCOPE_SUBTREE,
                                       settings.ORG_LDAP_FILTER,
                                       ldap_attrs )

    ldap_client.unbind_s()


    # i need to sort the list by last name so the presentation is more readable
    def sort_key( entry ):
        return ( entry[1]['sn'], entry[1]['givenName'] )

    ldap_users.sort( key = sort_key )

    return ldap_users

def not_allowed( request ):
    return render( request, "managerbase.html", {"message": "You are not allowed here"} )

def check_employee_login( request ):

    employee = None
    if request.user.is_authenticated():
        employee = Employee.objects.filter( user = request.user )
        if employee.count() == 1:
            return 0
        else:
            logout( request )
            return 1
    return 2

# this is called from other views if a a user isn't authenticated, the callback view allows to return to where the user wanted to go

def employee_login( request, callback_view ):

    login_status = check_employee_login( request )
    if login_status == 0:
        return  callback_view( request )
    elif login_status == 1:
        return render( request, "frontpage.html", {"message": "You have successfully authenticated but " +
                                                  "your time sheet account has not been created by " +
                                                  "the Office Manager. Please, request the account " +
                                                  "creation and log in again. Thank you."} )

    # this, if login_status == 2
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate( username = username, password = password )
        if user:
            login( request, user )
            return employee_login( request, callback_view )

    return render( request, "login_page.html" )

# should present a few options to user/manager/etc.
# listing function filtered on the user role
@csrf_exempt
def front_page( request ):

    if not request.user.is_authenticated():
        return employee_login( request, front_page )

    # in fact this needs to be passed as context to all pages of the system
    employee = Employee.objects.get( user = request.user )


    return render( request, "time_sheet_front.html", {'employee': employee} )

# time sheet preview and submission

def submit_time_sheet( request ):

    if not request.user.is_authenticated():
        return employee_login( request, submit_time_sheet )

    employee = Employee.objects.get( user = request.user )

    timesheet_data = timesheet.generate_timesheet_data( employee )
    timesheet_db = TimeSheet.objects.filter( employee = employee, period = timesheet_data['period'] )
    message = None
    # it the time sheet has already been submitted, correct information needs to be presented
    # with respect to balances
    if timesheet_db.count() > 0:
        timesheet_data = timesheet.generate_timesheet_data( employee, timesheet_db[0], False )
        message = 'This time sheet has already been submitted'


    if timesheet_data['salary_sources'] == {}:
        message = "Time sheet can't be submitted.\nSalary assignment is missing."

    if request.method == "POST":
        # check if already sumbitted
        if timesheet_data['salary_sources'] != {}:
            if timesheet_db.count() == 0:

                timesheet_obj = TimeSheet( 
                                      employee = employee,
                                      period = timesheet_data['period'],
                                      submit_date = datetime.date.today(),
                                      approve_date = None,
                                      start_date = timesheet_data['dates'][0],
                                      end_date = timesheet_data['dates'][1]
                                    )

                timesheet_obj.save()

                timesheet.send_notification( request, "SUBMITTED", timesheet_obj )

                message = 'Your time sheet for %s has been submitted for approval' % timesheet_data['period']




    return render( request, "time_sheet_submit.html", {'employee': employee,
                                                       "viewdata": timesheet_data,
                                                       "message": message} )


def request_leave( request ):

    if not request.user.is_authenticated():
        return employee_login( request, request_leave )


    employee = Employee.objects.get( user = request.user )
    time_sheet_data = timesheet.generate_timesheet_data( employee )

    if request.method != "POST":

        leave_form = models.LeaveForm()

    else:

        leave_form = models.LeaveForm( request.POST )
        if  leave_form.is_valid():

            leave_type = request.POST['type']
            start_date = request.POST['start_date']
            end_date = request.POST['end_date']


            date_start = [int( x ) for x in start_date.split( '-' )]
            date_end = [int( x ) for x in end_date.split( '-' )]
            date_start = datetime.date( date_start[0], date_start[1], date_start[2] )
            date_end = datetime.date( date_end[0], date_end[1], date_end[2] )

            if date_start > date_end:
                return render( request, "request_leave.html", {"employee": employee,
                                                               "form": leave_form,
                                                               "timesheet": time_sheet_data,
                                                               'message': "End date before Start date"} )
# # commented out for the sake of demonstration
#             if leave_type == 'HOLS':
#                 if date_start < datetime.date.today() or date_end < datetime.date.today():
#                     return render( request, "request_leave.html", {"employee": employee,
#                                                                    "form": leave_form,
#                                                                    "timesheet": time_sheet_data,
#                                                                    "message": "Vacation can not begin or end in the past"} )


            comment = request.POST['comment']

            leave_request = models.Leave( 
                                         type = leave_type,
                                         start_date = start_date,
                                         end_date = end_date,
                                         comment = comment,
                                         submit_date = datetime.date.today(),
                                         employee = employee )
            leave_request.save()

            timesheet.send_notification( request, "SUBMITTED", leave_request )

            return render( request, "time_sheet_front.html", {'employee': employee,
                                                              'message' : 'Your leave request has been submitted for approval',
                                                              "timesheet": time_sheet_data} )


    return render( request, "request_leave.html", {"employee": employee, "form": leave_form, "timesheet": time_sheet_data} )



def list_requests_to_approve( request ):

    if not request.user.is_authenticated():
        return employee_login( request, list_requests_to_approve )

    employee = Employee.objects.get( user = request.user )
    time_sheet_employee = None

    view_document = []
    view_data = None

    if request.method == "POST":

        if request.POST['button'] == "Approve Time Sheet":
            time_sheet = TimeSheet.objects.get( id = request.POST['id'] )

            # update employee balances
            time_sheet_employee = Employee.objects.get( id = time_sheet.employee.id )
            time_sheet_data = timesheet.generate_timesheet_data( time_sheet_employee, time_sheet )
            time_sheet_employee.leave_balance_HOLS = time_sheet_data['leave_data'][6]
            time_sheet_employee.leave_balance_SICK = time_sheet_data['leave_data'][7]
            time_sheet_employee.save()

            # save the time sheet
            time_sheet.approve_date = datetime.date.today()
            time_sheet.approved_by = request.user.first_name + ' ' + request.user.last_name

            # save current SICK and HOLS balances to the timesheet
            time_sheet.leave_earn_HOLS = time_sheet_data['leave_data'][2]
            time_sheet.leave_earn_SICK = time_sheet_data['leave_data'][3]
            time_sheet.leave_used_HOLS = time_sheet_data['leave_data'][4]
            time_sheet.leave_used_SICK = time_sheet_data['leave_data'][5]
            time_sheet.leave_balance_HOLS = time_sheet_data['leave_data'][6]
            time_sheet.leave_balance_SICK = time_sheet_data['leave_data'][7]

            time_sheet.save()

            send_notification( request, 'APPROVED', time_sheet )


        if request.POST['button'] == "Approve Leave Request":
            leave = Leave.objects.get( id = request.POST['id'] )
            leave.approve_date = datetime.date.today()
            leave.approved_by = request.user.first_name + ' ' + request.user.last_name
            leave.save()

            send_notification( request, 'APPROVED', leave )

        if request.POST['button'] == "View Leave Request":
            leave_request = Leave.objects.get( id = request.POST['id'] )
            leave_request.type = dict( leave_request.TYPES )[leave_request.type]
            view_document = {'type' : "LEAVE_REQUEST", 'data' : leave_request}

        if request.POST['button'] == "View Time Sheet":
            time_sheet = TimeSheet.objects.get( id = request.POST['id'] )
            time_sheet_employee = Employee.objects.get( id = time_sheet.employee.id )
            view_document = {'type' : "TIME_SHEET", 'data' : time_sheet}
            view_data = timesheet.generate_timesheet_data( time_sheet_employee, time_sheet )


    documents = timesheet.documents_to_approve( request )

    message = None

    if documents['time_sheets'].count() == 0 and documents['leave_requests'].count() == 0:
        message = "You don't have any documents to approve"

    return render( request, "documents_to_approve.html", {"employee" : employee,
                                                          "documents" : documents,
                                                          "viewdocument" : view_document,
                                                          "viewdata" : view_data,
                                                          "timesheetemployee" : time_sheet_employee,
                                                          "message": message} )





def manage_salary_sources( request ):

    if not request.user.is_authenticated():
        return employee_login( request, manage_salary_sources )

    employee = Employee.objects.get( user = request.user )

    if employee.role != 'OMAN' and employee.role != 'FMAN':
        return not_allowed( request )

    edited_id = ""
    form = SalarySourceForm()

    if request.method == "POST":

        if request.POST.has_key( 'button' ):

            if request.POST['button'] == "Edit":
                edited_id = request.POST['id']
                form.fields['code'].initial = SalarySource.objects.get( id = request.POST['id'] ).code

            elif request.POST['button'] == "Delete":
                SalarySource.objects.get( id = request.POST['id'] ).delete()
        else:
            if request.POST['edited_id'] == "":
                salary_source = SalarySource()
                salary_source.code = request.POST['code']
                if salary_source.code.strip() != '':
                    salary_source.save()
            else:
                salary_source = SalarySource.objects.get( id = request.POST['edited_id'] )
                salary_source.code = request.POST['code']
                if salary_source.code.strip() != '':
                    salary_source.save()


    salary_sources = SalarySource.objects.all()

    return render( request, "salary_sources.html", {"employee":employee,
                                                    "form": form,
                                                    "sourcelist": salary_sources,
                                                    "edited_id": edited_id
                                                    } )





def assign_salary_sources( request ):

    if not request.user.is_authenticated():
        return employee_login( request, assign_salary_sources )

    employee = Employee.objects.get( user = request.user )

    if employee.role != 'OMAN' and employee.role != 'FMAN':
        return not_allowed( request )

    # pylint: disable=no-member
    users = User.objects.all()

    employee_list = Employee.objects.filter( user = users ).order_by( 'user__last_name' )

    salary_sources = SalarySource.objects.all()

    time_sheet_data = timesheet.generate_timesheet_data( employee )

    curr_employee = None
    message = None

    if request.method == "POST":
        if request.POST['button'] == "Submit":
            assignment_sum = 0
            for s_source in salary_sources:
                assignment_sum += int( request.POST["amount-" + s_source.code] )

            if assignment_sum == 100:

                for s_source in salary_sources:
                    current_assignment = SalaryAssignment.objects.filter( 
                                             source = SalarySource.objects.get( code = s_source.code ),
                                             employee = Employee.objects.get( id = request.POST["employee"] ),
                                             period = time_sheet_data['period']
                                            )
                    if current_assignment.count() == 1:
                        current_assignment = SalaryAssignment.objects.get( 
                                             source = SalarySource.objects.get( code = s_source.code ),
                                             employee = Employee.objects.get( id = request.POST["employee"] ),
                                             period = time_sheet_data['period']
                                            )
                        current_assignment.percentage = request.POST["amount-" + s_source.code]
                        current_assignment.save()
                    else:

                        current_assignment = SalaryAssignment( 
                                                     source = SalarySource.objects.get( code = s_source.code ),
                                                     employee = Employee.objects.get( id = request.POST["employee"] ),
                                                     period = time_sheet_data['period'],
                                                     percentage = request.POST["amount-" + s_source.code] )

                        current_assignment.save()

                send_notification( request, "SALARY_ASSIGNED", current_assignment )

            else:
                message = "The assignments must amount to 100%"

        # retrieve data to present correct value in the table


        listed_employee = Employee.objects.get( id = request.POST["employee"] )
        empl_assignments = SalaryAssignment.objects.filter( 
                                         employee = Employee.objects.get( id = request.POST["employee"] ),
                                         period = time_sheet_data['period'] )
        assign_dict = {}
        for assign in empl_assignments:
            assign_dict[assign.source.code] = assign.percentage

        curr_employee = {'employee':listed_employee, 'assign': assign_dict}



    salary_assignments = SalaryAssignment.objects.filter( period = time_sheet_data['period'] )







    return render( request, "assign_salary.html", {"employee": employee,
                                                   "employee_list": employee_list,
                                                   "salary_sources": salary_sources,
                                                   "percentage_choice": range( 101 ),
                                                   "period": time_sheet_data['period'],
                                                   "assignments": salary_assignments,
                                                   "currentemployee": curr_employee,
                                                   "message": message} )




def manage_users( request ):

    if not request.user.is_authenticated():
        return employee_login( request, manage_users )

    employee = Employee.objects.get( user = request.user )

    if employee.role != 'OMAN':
        return not_allowed( request )


    available_accounts = available_user_list()
    available_roles = employee.ROLES


    defaults = {"role":"EMPL",
                "start_time":"10:00",
                "end_time":"18:00",
                "location":"Tbilisi",
                "break_hours":"1",
                }



    message = None
    userdata = None


    existing_accounts = Employee.objects.all().order_by( 'user__last_name' )


    # a few cases here, create, update, defaults for not existing
    if request.method == "POST":

        userdata = {}

        if request.POST['button'] == "Update View":
            userdata['username'] = request.POST['account-name']

            # pylint: disable=no-member
            user = user = User.objects.filter( username = request.POST['account-name'] )
            if user.count() == 1:
                user = User.objects.get( username = request.POST['account-name'] )
                u_employee = Employee.objects.filter( user = user )

                if u_employee.count() == 1:
                    u_employee = Employee.objects.get( user = user )
                    userdata['position'] = u_employee.position
                    userdata['role'] = u_employee.role
                    userdata['supervisor'] = u_employee.supervisor.username
                    userdata['start_time'] = u_employee.workday_start
                    userdata['end_time'] = u_employee.workday_end
                    userdata['break_hours'] = u_employee.break_hours
                    userdata['location'] = u_employee.location
                    userdata['leave_hols'] = u_employee.leave_balance_HOLS
                    userdata['leave_sick'] = u_employee.leave_balance_SICK
                else:
                    message = "New Employee"
            else:
                message = "New Employee"

        # create employee or update data
        if request.POST['button'] == "Create or Update":
            # check what's there what's not there
            check_fields = {"position":"POSITION",
                            "start-time": "WORKDAY_START",
                            "end-time": "WORKDAY_END",
                            "break-hours": "BREAK_HOURS",
                            "location": "LOCATION",
                            "leave-hols": "VACATION_BALANCE",
                            "leave-sick": "SICK_BALANCE"}

            error_message = "Incomplete data. Missing: "
            error = False
            for key in check_fields:
                if request.POST[key] == "":
                    error_message += " " + check_fields[ key]
                    error = True

            if error:
                message = error_message
                viewdata = {"accounts": available_accounts,
                            "roles": available_roles,
                            "employees": existing_accounts,
                            "defaults": defaults,
                            "userdata": userdata}
                return render( request, "manage_users.html", {'employee': employee,
                                                              'message': message,
                                                              "viewdata": viewdata} )

            # pylint: disable=no-member
            user = User.objects.filter( username = request.POST['account-name'] )
            if user.count() == 1:
                user = User.objects.get( username = request.POST['account-name'] )
            else:
                user = LDAPBackend().populate_user( request.POST['account-name'] )
                user = User.objects.get( username = request.POST['account-name'] )
                user.save()

            u_employee = Employee.objects.filter( user = user )

            if u_employee.count() == 1:
                u_employee = Employee.objects.get( user = user )
            else:
                u_employee = Employee( user = user )

            # here a lot of checking
            u_employee.position = request.POST['position']
            u_employee.role = request.POST['role']

            super_user = User.objects.filter( username = request.POST['super-name'] )
            if super_user.count() == 1:
                super_user = User.objects.get( username = request.POST['super-name'] )
            else:
                super_user = LDAPBackend().populate_user( request.POST['super-name'] )
                super_user = User.objects.get( username = request.POST['super-name'] )
                super_user.save()

            u_employee.supervisor = super_user
            u_employee.location = request.POST['location']
            u_employee.workday_start = request.POST['start-time']
            u_employee.workday_end = request.POST['end-time']
            u_employee.break_hours = request.POST['break-hours']
            u_employee.leave_balance_HOLS = request.POST['leave-hols']
            u_employee.leave_balance_SICK = request.POST['leave-sick']
            u_employee.leave_balance_MATL = 0
            u_employee.leave_balance_PATL = 0
            u_employee.leave_balance_UNPD = 0

            u_employee.save()

            u_employee = Employee.objects.get( user = user )
            userdata = {}
            userdata['username'] = u_employee.user.username
            userdata['position'] = u_employee.position
            userdata['role'] = u_employee.role
            userdata['supervisor'] = u_employee.supervisor.username
            userdata['start_time'] = u_employee.workday_start
            userdata['end_time'] = u_employee.workday_end
            userdata['break_hours'] = u_employee.break_hours
            userdata['location'] = u_employee.location
            userdata['leave_hols'] = u_employee.leave_balance_HOLS
            userdata['leave_sick'] = u_employee.leave_balance_SICK

            message = "Employee %s saved." % u_employee.user.username


    viewdata = {"accounts": available_accounts,
                "roles": available_roles,
                "employees": existing_accounts,
                "defaults": defaults,
                "userdata": userdata}

    return render( request, "manage_users.html", {'employee': employee,
                                                  'message': message,
                                                  "viewdata": viewdata} )


def approved_documents( request ):
    if not request.user.is_authenticated():
        return employee_login( request, approved_documents )

    employee = Employee.objects.get( user = request.user )

    if employee.role != 'OMAN':
        return not_allowed( request )

    message = None
    
    
    # dropdown with periods,have to do direct db query
    from django.db import connection
    cursor = connection.cursor()
    cursor.execute( "select distinct period from \"TimeSheetManager_timesheet\"")
    period_list = cursor.fetchall()[0]
    periods = []
    for period in period_list:
        periods.append({"period": period})
        
        
        

    # dropdown with types of document types is defined in the template

    # dropdown with employees
    employees = Employee.objects.all().order_by('user__first_name')

    document_types = {"ALL": "All",
                      "TIMESHEET": "Time sheet",
                      "LEAVEREQUEST": "Leave request",
                      "SALARYASSIGNMENT": "Salary assignment"}


    viewdata = {"periods": periods,
                "employees": employees,
                "documenttypes" : document_types,
                }

    reportdata = {"report_period": periods[0]['period'],
                  "report_employee": "All",
                  "report_document": "ALL"}

    documents = {}

    if request.method == "POST":
        reportdata["report_period"] = report_period = request.POST['data-period']
        reportdata["report_document"] = report_document = request.POST['document-type']
        reportdata["report_employee"] = report_employee = request.POST['employee']


        # pylint: disable=no-member
        if report_employee == "All":
            report_employee = Employee.objects.all()
        else:
            report_user = User.objects.get( username = report_employee )
            report_employee = [Employee.objects.get( user = report_user )]

        if report_period == "All":
            report_period = period_list

            # report dates
            month, year = period_list[0].split( ' ' )
            month_number = timesheet.months.index( month ) + 1
            start_date = datetime.date( int( year ), month_number, 1 )

            month, year = period_list[-1].split( ' ' )
            month_number = timesheet.months.index( month ) + 1
            end_date = datetime.date( int( year ), month_number + 1, 1 ) - datetime.timedelta( days = 1 )

        else:
            report_period = [report_period]
            # report dates
            month, year = period_list[0].split( ' ' )
            month_number = timesheet.months.index( month ) + 1
            start_date = datetime.date( int( year ), month_number, 1 )

            end_date = datetime.date( int( year ), month_number + 1, 1 ) - datetime.timedelta( days = 1 )


        if report_document == "ALL" or report_document == "TIMESHEET":
            time_sheets = TimeSheet.objects.filter( employee__in = report_employee,
                                                    period__in = report_period,
                                                    approve_date__isnull = False )

            documents['timesheets'] = []
            for time_sheet in time_sheets:
                document = {}
                document['timesheet'] = time_sheet
                document['viewdata'] = timesheet.generate_timesheet_data( time_sheet.employee, time_sheet, True )


                documents['timesheets'].append( document )
        else:
            documents['timesheets'] = None







        if report_document == "ALL" or report_document == "LEAVEREQUEST":
            leave_requests = []
            for each_employee in report_employee:
                l_requests = timesheet.find_leave_requests( each_employee, ( start_date, end_date ) )
                leave_requests.append( l_requests['requests'] )

            documents['leaverequests'] = []
            for req_list in leave_requests:
                for l_req in req_list:
                    l_req.type = dict( l_req.TYPES )[ l_req.type]
                    documents['leaverequests'].append( {"data": l_req} )

        else:
            documents['leaverequests'] = None





        if report_document == "ALL" or report_document == "SALARYASSIGNMENT":
            if reportdata["report_period"] == 'All':
                salary_assigments = SalaryAssignment.objects.all()
            else:
                salary_assigments = SalaryAssignment.objects.filter( period = reportdata["report_period"] )

            documents['employeelist'] = report_employee
            documents['periodlist'] = period_list
            documents['salarysources'] = SalarySource.objects.all()

        else:
            salary_assigments = None

        documents['salaryassignments'] = salary_assigments



        reportdata['documents'] = documents


#         message = documents['leaverequests']

    return render( request, "approved_documents.html", {"employee" : employee,
                                                        "message": message,
                                                        "viewdata": viewdata,
                                                        "reportdata": reportdata} )
