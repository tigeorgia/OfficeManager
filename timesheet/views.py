from django.shortcuts import render
from employee.views import checkuserloggedin
from timesheet import tshelpers
from models import TimeSheet
import datetime

@checkuserloggedin
def submit_time_sheet( request, employee ):

    # default period is current month
    months = tshelpers.months

    today = datetime.date.today()

    period = '%s %d' % ( months[ today.month - 1], today.year )

    availableperiods = []
    for month in months:
        availableperiods.append( '%s %d' % ( month, today.year ) )

    timesheet_data = None
    message = ''


    if request.method == "POST":

        period = request.POST['period']
        timesheet_data = tshelpers.generate_timesheet_data( employee, period )

        timesheet_db = TimeSheet.objects.filter( employee = employee, period = timesheet_data['period'] )
        message = None
        # it the time sheet has already been submitted, correct information needs to be presented
        # with respect to balances

        if timesheet_db.count() > 0:
            timesheet_data = tshelpers.generate_timesheet_data( employee, period, timesheet_db[0], False )
            message = 'This time sheet has already been submitted'


        if timesheet_data['salary_sources'] == {}:
            message = "Time sheet can't be submitted.\nSalary assignment is missing."


        if request.POST['button'] == 'Submit':
            # check if already sumbitted
            if timesheet_data['salary_sources'] != {}:
                if timesheet_db.count() == 0:


                    # need to calculate balances and use them here
                    timesheet_obj = TimeSheet( 
                                          employee = employee,
                                          period = timesheet_data['period'],
                                          submit_date = datetime.date.today(),
                                          approve_date = None,
                                          start_date = timesheet_data['dates'][0],
                                          end_date = timesheet_data['dates'][1]
                                        )


                    timesheet_obj.leave_balance_before_HOLS = timesheet_data['leave_data'][0]
                    timesheet_obj.leave_balance_before_SICK = timesheet_data['leave_data'][1]
                    timesheet_obj.leave_earn_HOLS = timesheet_data['leave_data'][2]
                    timesheet_obj.leave_earn_SICK = timesheet_data['leave_data'][3]
                    timesheet_obj.leave_used_HOLS = timesheet_data['leave_data'][4]
                    timesheet_obj.leave_used_SICK = timesheet_data['leave_data'][5]
                    timesheet_obj.leave_balance_HOLS = timesheet_data['leave_data'][6]
                    timesheet_obj.leave_balance_SICK = timesheet_data['leave_data'][7]




                    timesheet_obj.save()



                    tshelpers.send_notification( request, "SUBMITTED", timesheet_obj )

                    message = 'Your time sheet for %s has been submitted for approval' % timesheet_data['period']




    return render( request, "time_sheet_submit.html", {'employee': employee,
                                                       'period' : period,
                                                       'availableperiods' : availableperiods,
                                                       'timesheetdata': timesheet_data,
                                                       'viewdata' : timesheet_data,
                                                       'message' : message,
                                                       } )




