from django.shortcuts import render
import ldap
from OfficeManager import settings
from employee.models import Profile
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django_auth_ldap.backend import LDAPBackend

# decorator for all methods than need a user to be logged in
def checkuserloggedin( func ):

    def checklogin( request ):
        if not request.user.is_authenticated():
            return employee_login( request, func )
        else:
            employee = Profile.objects.get( user = request.user )
            return func( request, employee )

    return checklogin


@checkuserloggedin
def manage_profile( request, employee ):

    employee_list = available_user_list()

    profile_editable = None
    if employee.role == '2-OMAN':
        profile_editable = False # should be exactly the oposite, this is for tests
        
    # if none other selected
    edited_employee = employee

    




    return render( request, 
                   "manage_profile.html", 
                   {
                    "employee": employee,
                    "employeelist": employee_list,
                    "editedemployee": edited_employee,
                    "editable": profile_editable,
                    } 
                  )




# a little ldap helper
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
        employee = Profile.objects.filter( user = request.user )
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
        employee = Profile.objects.get( user = request.user )
        return  callback_view( request, employee )
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

@checkuserloggedin
def manage_users( request, employee ):


    if employee.role != '2-OMAN':
        return not_allowed( request )


    available_accounts = available_user_list()
    available_roles = employee.ROLES


    defaults = {"role":"EMPL",
                "start_time":"10:00",
                "end_time":"18:00",
                "location":"Tbilisi",
                }



    message = None
    userdata = None


    existing_accounts = Profile.objects.all().order_by( 'user__last_name' )


    # a few cases here, create, update, defaults for not existing
    if request.method == "POST":

        userdata = {}

        if request.POST['button'] == "Update View":
            userdata['username'] = request.POST['account-name']

            # pylint: disable=no-member
            user = user = User.objects.filter( username = request.POST['account-name'] )
            if user.count() == 1:
                user = User.objects.get( username = request.POST['account-name'] )
                u_employee = Profile.objects.filter( user = user )

                if u_employee.count() == 1:
                    u_employee = Profile.objects.get( user = user )
                    userdata['position'] = u_employee.position
                    userdata['role'] = u_employee.role
                    userdata['supervisor'] = u_employee.supervisor.username
                    userdata['start_time'] = u_employee.workday_start
                    userdata['end_time'] = u_employee.workday_end
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

            u_employee = Profile.objects.filter( user = user )

            if u_employee.count() == 1:
                u_employee = Profile.objects.get( user = user )
            else:
                u_employee = Profile( user = user )

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

            u_employee = Profile.objects.get( user = user )
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

