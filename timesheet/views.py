from django.shortcuts import render
from employee.views import employee_login
from employee.models import Profile
from timesheet import tshelpers
from models import TimeSheet
import timesheet
import datetime

def submit_time_sheet( request ):

    if not request.user.is_authenticated():
        return employee_login( request, submit_time_sheet )

    employee = Profile.objects.get( user = request.user )

    timesheet_data = tshelpers.generate_timesheet_data( employee )
    timesheet_db = TimeSheet.objects.filter( employee = employee, period = timesheet_data['period'] )
    message = None
    # it the time sheet has already been submitted, correct information needs to be presented
    # with respect to balances
    if timesheet_db.count() > 0:
        timesheet_data = tshelpers.generate_timesheet_data( employee, timesheet_db[0], False )
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

                tshelpers.send_notification( request, "SUBMITTED", timesheet_obj )

                message = 'Your time sheet for %s has been submitted for approval' % timesheet_data['period']




    return render( request, "time_sheet_submit.html", {'employee': employee,
                                                       "viewdata": timesheet_data,
                                                       "message": message} )

