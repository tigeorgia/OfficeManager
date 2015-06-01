from django.shortcuts import render

from employee.views import employee_login, not_allowed
from budgetshare.models import SalarySourceForm, SalarySource, SalaryAssignment
from django.contrib.auth.models import User
from timesheet.tshelpers import generate_timesheet_data, send_notification
from employee.models import Profile
from frontpage.views import checkuserloggedin




@checkuserloggedin
def import_salary_assignments( request ):

    #----------------------------------- if not request.user.is_authenticated():
        #----------- return employee_login( request, import_salary_assignments )

    employee = Profile.objects.get( user = request.user )

    return render( request, "import_salary_assignments.html", { "employee": employee} )










@checkuserloggedin
def manage_salary_sources( request ):

    employee = Profile.objects.get( user = request.user )

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




@checkuserloggedin
def assign_salary_sources( request ):



    employee = Profile.objects.get( user = request.user )

    if employee.role != 'OMAN' and employee.role != 'FMAN':
        return not_allowed( request )

    # pylint: disable=no-member
    users = User.objects.all()

    employee_list = Profile.objects.filter( user = users ).order_by( 'user__last_name' )

    salary_sources = SalarySource.objects.all()

    time_sheet_data = generate_timesheet_data( employee )

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
                                             employee = Profile.objects.get( id = request.POST["employee"] ),
                                             period = time_sheet_data['period']
                                            )
                    if current_assignment.count() == 1:
                        current_assignment = SalaryAssignment.objects.get( 
                                             source = SalarySource.objects.get( code = s_source.code ),
                                             employee = Profile.objects.get( id = request.POST["employee"] ),
                                             period = time_sheet_data['period']
                                            )
                        current_assignment.percentage = request.POST["amount-" + s_source.code]
                        current_assignment.save()
                    else:

                        current_assignment = SalaryAssignment( 
                                                     source = SalarySource.objects.get( code = s_source.code ),
                                                     employee = Profile.objects.get( id = request.POST["employee"] ),
                                                     period = time_sheet_data['period'],
                                                     percentage = request.POST["amount-" + s_source.code] )

                        current_assignment.save()

                send_notification( request, "SALARY_ASSIGNED", current_assignment )

            else:
                message = "The assignments must amount to 100%"

        # retrieve data to present correct value in the table


        listed_employee = Profile.objects.get( id = request.POST["employee"] )
        empl_assignments = SalaryAssignment.objects.filter( 
                                         employee = Profile.objects.get( id = request.POST["employee"] ),
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





