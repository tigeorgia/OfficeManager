from django.shortcuts import render
from employee.views import not_allowed, checkuserloggedin
from employee.models import Profile
from timesheet.models import TimeSheet
from timesheet import tshelpers
import datetime
from timesheet.tshelpers import send_notification, months
from leaverequest.models import Leave
from django.contrib.auth.models import User
from budgetshare.models import SalaryAssignment, SalarySource
from datetime import timedelta

@checkuserloggedin
def list_requests_to_approve( request, employee ):

    time_sheet_employee = None

    view_document = []
    view_data = None

    if request.method == "POST":

        if request.POST['button'] == "Approve Time Sheet":
            time_sheet = TimeSheet.objects.get( id = request.POST['id'] )

            # update employee balances
            time_sheet_employee = Profile.objects.get( id = time_sheet.employee.id )
            time_sheet_data = tshelpers.generate_timesheet_data( time_sheet_employee, time_sheet.period, time_sheet )
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


        if request.POST['button'] == "Decline Leave Request":
            leave = Leave.objects.get( id = request.POST['id'] )
            leave.approve_date = datetime.date.today()
            leave.approved_by = request.user.first_name + ' ' + request.user.last_name
            leave.declined = True
            leave.save()

            send_notification( request, 'DECLINED', leave )

        if request.POST['button'] == "Approve Leave Request":
            leave = Leave.objects.get( id = request.POST['id'] )
            leave.approve_date = datetime.date.today()
            leave.approved_by = request.user.first_name + ' ' + request.user.last_name
            leave.save()

            if leave.type == "HOLS":
                leave.employee.leave_balance_HOLS -= leave.workdays_requested

            if leave.type == "SICK":
                leave.employee.leave_balance_SICK -= leave.workdays_requested

            leave.employee.save()


            send_notification( request, 'APPROVED', leave )

        if request.POST['button'] == "View Leave Request":
            leave_request = Leave.objects.get( id = request.POST['id'] )
            leave_request.type = dict( leave_request.TYPES )[leave_request.type]
            view_document = {'type' : "LEAVE_REQUEST", 'data' : leave_request}

        if request.POST['button'] == "View Time Sheet":
            time_sheet = TimeSheet.objects.get( id = request.POST['id'] )
            time_sheet_employee = Profile.objects.get( id = time_sheet.employee.id )
            view_document = {'type' : "TIME_SHEET", 'data' : time_sheet}
            view_data = tshelpers.generate_timesheet_data( time_sheet_employee, time_sheet.period, time_sheet )


    documents = tshelpers.documents_to_approve( request )

    message = None

    if documents['time_sheets'].count() == 0 and documents['leave_requests'].count() == 0:
        message = "You don't have any documents to approve"

    return render( request, "documents_to_approve.html", {"employee" : employee,
                                                          "documents" : documents,
                                                          "viewdocument" : view_document,
                                                          "viewdata" : view_data,
                                                          "timesheetemployee" : time_sheet_employee,
                                                          "message": message} )


def define_period_list( employee ):

    periods = []
#     from django.db import connection
#     cursor = connection.cursor()
#     cursor.execute( "select distinct period from \"timesheet_timesheet\"")
#     period_list = cursor.fetchall()

    # start and end of leave requests
    
    leave_requests = Leave.objects.filter( approve_date__isnull = False).order_by( "start_date" )
    if leave_requests:
        lr_start_date = leave_requests[0].start_date
    else:
        lr_start_date = datetime.date.today()

    leave_requests = Leave.objects.filter( approve_date__isnull = False).order_by( "-end_date" )
    
    if leave_requests:
        lr_end_date = leave_requests[0].end_date
    else:
        lr_end_date = datetime.date.today()

    # start and end of timesheets

    time_sheets = TimeSheet.objects.filter( approve_date__isnull = False).order_by( "start_date" )

    if time_sheets:
        ts_start_date = time_sheets[0].start_date
        ts_end_date = time_sheets[-1].end_date
    else:
        ts_start_date = ts_end_date = datetime.date.today()


    start_date = min( lr_start_date, ts_start_date )
    end_date = max( lr_end_date, ts_end_date )
    start_date -= timedelta( days = start_date.day - 1)
    end_date -= timedelta( days = end_date.day - 1)


    current_date = start_date
    while True:
        period = '%s %d' % ( months[ current_date.month - 1 ], current_date.year )
        periods.append( period)

        current_date += timedelta( days = 32 )
        current_date -= timedelta( days = current_date.day - 1)

        if current_date > end_date:
            break



    periods.reverse()
    return periods


@checkuserloggedin
def approved_documents( request, employee ):


    #     if employee.role != '2-OMAN':
    #         return not_allowed( request )

    message = None


    # dropdown with periods,have to do direct db query


    period_list = define_period_list( employee )


    periods = []
    if period_list:
        for period in period_list:
            periods.append( {"period": period} )

    #--------------------------------------------------------------------- else:
        #------------------------------- # faking it because the system is empty
        #----------------------------------- month = datetime.date.today().month
        #------------------------------------- year = datetime.date.today().year
        # period_list = ['%s %d' % ( tshelpers.months[month - 1],  year)] #something for the current month


    # dropdown with types of document types is defined in the template

    # dropdown with employees
    employees = Profile.objects.all().order_by( 'user__last_name' )

    document_types = {"ALL": "All",
                      "TIMESHEET": "Time sheet",
                      "LEAVEREQUEST": "Leave request",
                      "SALARYASSIGNMENT": "Salary assignment"}


    viewdata = {
                "periods": periods,
                "employees": employees,
                "documenttypes" : document_types,
                }


    if periods != []:
        today_date = datetime.date.today()
    
        report_period =  '%s %d' % ( months[today_date.month - 1], today_date.year)
    else:
        report_period = 'ALL'

    reportdata = {"report_period": report_period,
                  "report_employee": employee.user.username,
                  "report_document": "ALL"}


    documents = {}

    if request.method == "POST":
        reportdata["report_period"] = report_period = request.POST['data-period']
        reportdata["report_document"] = report_document = request.POST['document-type']
        if request.POST.has_key( "report-employee" ):
            reportdata["report_employee"] = report_employee = request.POST['report-employee']
        else:
            reportdata["report_employee"] = report_employee = employee.user.username

        if period_list:
            # pylint: disable=no-member
            if report_employee == "All":
                report_employee = Profile.objects.all()
            else:
                report_user = User.objects.get( username = report_employee )
                report_employee = [Profile.objects.get( user = report_user )]

            if report_period == "All":
                report_period = period_list

                # report dates
                month, year = period_list[-1].split( ' ' )
                month_number = tshelpers.months.index( month ) + 1
                start_date = datetime.date( int( year ), month_number, 1 )

                month, year = period_list[0].split( ' ' )
                month_number = tshelpers.months.index( month ) + 1
                end_date = datetime.date( int( year ), month_number + 1, 1 ) - datetime.timedelta( days = 1 )

            else:
                report_period = [report_period]
                # report dates
                month, year = report_period[0].split( ' ' )
                month_number = tshelpers.months.index( month ) + 1
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
                    document['viewdata'] = tshelpers.generate_timesheet_data( time_sheet.employee, time_sheet.period, time_sheet, True )


                    documents['timesheets'].append( document )
            else:
                documents['timesheets'] = None







            if report_document == "ALL" or report_document == "LEAVEREQUEST":
                leave_requests = []
                for each_employee in report_employee:
                    l_requests = tshelpers.find_leave_requests( each_employee, ( start_date, end_date ) )
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
        else:
            message = "There is no data in the system"

#         message = documents['leaverequests']

    return render( request, "approved_documents.html", {"employee" : employee,
                                                        "message": message,
                                                        "viewdata": viewdata,
                                                        "reportdata": reportdata} )
