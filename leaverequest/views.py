from django.shortcuts import render
from employee.views import checkuserloggedin
from employee.models import Profile
from timesheet import tshelpers
from leaverequest import models
import datetime

@checkuserloggedin
def request_leave( request ):


    employee = Profile.objects.get( user = request.user )
    time_sheet_data = tshelpers.generate_timesheet_data( employee )

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

            tshelpers.send_notification( request, "SUBMITTED", leave_request )

            return render( request, "time_sheet_front.html", {'employee': employee,
                                                              'message' : 'Your leave request has been submitted for approval',
                                                              "timesheet": time_sheet_data} )


    return render( request, "request_leave.html", {"employee": employee, "form": leave_form, "timesheet": time_sheet_data} )


