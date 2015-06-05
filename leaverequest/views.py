from django.shortcuts import render
from employee.views import checkuserloggedin
from leaverequest.models import LeaveForm, Leave
from django.utils.datetime_safe import datetime
from publicholidays.models import PublicHoliday
from datetime import timedelta
from timesheet.tshelpers import send_notification


@checkuserloggedin
def request_leave( request, employee ):

    message = ''


    if request.method == "POST":
        leave_form = LeaveForm( request.POST )

        if leave_form.is_valid():
            
            leave_request = Leave(
                                  start_date = datetime.strptime( request.POST["start_date"], '%Y-%m-%d' ),
                                  end_date = datetime.strptime( request.POST["end_date"], '%Y-%m-%d' ),
                                  employee = employee,
                                  type = request.POST["type"],
                                  comment = request.POST["comment"],
                                  submit_date = datetime.today(),
                                  approved_by = employee.supervisor.first_name + ' ' + employee.supervisor.last_name
                                  )

            working_days = count_working_days( leave_request )

            message = "%s Leave request for %d working days has been submitted for approval." % (
                                                                                               dict( leave_request.TYPES)[ leave_request.type],
                                                                                               working_days,
                                                                                               )
            
            
            hols_result = employee.leave_balance_HOLS
            if leave_request.type == 'HOLS':
                hols_result -= working_days
                
            sick_result = employee.leave_balance_SICK
            if leave_request.type == 'SICK':
                sick_result -= working_days
            
            
            
            message += '\nYour resulting balance will be Vacation: %d, Sick %.2f' % (hols_result, sick_result)
            
            leave_request.save()
            
            send_notification( request, "SUBMITTED", leave_request )

    else:
        leave_form = LeaveForm()


    return render( request, "request_leave.html", {
                                                   "employee": employee,
                                                   "form": leave_form,
                                                   "message": message,
                                                   } )


def count_working_days( leave_request ):
    start_date = leave_request.start_date
    end_date = leave_request.end_date


    holidays = PublicHoliday.objects.filter( date__gte = start_date
                                             ).filter( date__lte = end_date)

    holiday_count = 0
    
    for holiday in holidays:
        if holiday.date.weekday() < 5 and holiday.type == "Public holiday":
            holiday_count += 1
        
    current_date = start_date
    
    workday_count = 0
    while True:
        if current_date.weekday() < 5:
            workday_count += 1
            
        if current_date == end_date:
            break
        
        current_date += timedelta( days = 1) 
        
    
    workday_count -= holiday_count
    
    return workday_count
    
