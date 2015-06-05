from django.shortcuts import render
import ldap
from OfficeManager import settings
from employee.models import Profile
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django_auth_ldap.backend import LDAPBackend
import os
from attachment.models import ProfileAttachment
from django.utils.datetime_safe import datetime

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
        profile_editable = True  # should be exactly the opposite, this is for tests

    # if none other selected
    edited_employee = employee
    message = ''

    if request.method == 'POST':

        if request.POST.has_key("button"):

            if request.POST['button'].upper() == "UPDATE VIEW":
    
                profile_data = update_profile_data( request.POST )
                message = profile_data['message']
                edited_employee = profile_data['user-profile']
    
            if request.POST['button'].upper() == "SAVE PROFILE":
    
                save_result = save_profile_to_database( request )
                edited_employee = save_result['profile']
                message = save_result["message"]

        if request.POST.has_key("delete-attachment"):
            # delete attachment
            attachment = ProfileAttachment.objects.get( id = request.POST['delete-attachment'])
            attachment.delete()
                
            


    attachments = ProfileAttachment.objects.filter( profile = edited_employee)

    return render( request,
                   "manage_profile.html",
                   {
                    "employee": employee,
                    "employeelist": employee_list,
                    "editedemployee": edited_employee,
                    "editable": profile_editable,
                    "message": message,
                    "attachments": attachments,

                    }
                  )



def save_profile_to_database( request ):

    post_data = request.POST
    # profile modeldata
    profile = Profile.objects.get_or_create( user__id = post_data["user-id"] )
    profile = profile[0]

    profile.position = post_data["position"]
    profile.location = post_data["location"]
    profile.seniority = post_data["seniority"]

    supervisor = LDAPBackend().populate_user( post_data['supervisor'] )
    profile.supervisor = supervisor

    profile.employment_status = post_data["empl-status"]
    profile.contract_start = datetime.strptime( post_data["contract-start"], '%Y-%m-%d') 
    profile.contract_end = datetime.strptime( post_data["contract-end"], '%Y-%m-%d') 
    profile.salary_gross_usd = post_data["salary-gross"]
    profile.salary_net_usd = post_data["salary-net"]

    profile.insurance = False
    if post_data["insurance"] == "True":
        profile.insurance = True

    profile.gsm_limit = post_data["gsm-limit"]
    profile.role = post_data["system-role"]

    profile.mobile_num = post_data["mobile-num"]
    profile.personal_num = post_data["personal-num"]
    profile.date_of_birth = datetime.strptime( post_data["date-of-birth"], '%Y-%m-%d') 
    profile.address = post_data["address"]

    profile.leave_balance_HOLS = post_data["leave-hols"]
    profile.leave_balance_SICK = post_data["leave-sick"]

    try:
        profile.save()
        
        message = "Profile data has been saved"

        if request.FILES:
            # handle picture upload
            if request.FILES.has_key('picture'):
                target_dir = settings.MEDIA_ROOT + '/profile/%s' % profile.user.username
                save_file( request, target_dir, request.FILES['picture'], profile )
    
                profile.picture = "profile/%s/%s" % ( profile.user.username, request.FILES['picture'].name)
                profile.save()
        
            # handle document attachment
            if request.FILES.has_key('attachment-file'):
                target_dir = settings.MEDIA_ROOT + '/attachments/%s' % profile.user.username
                save_file( request, target_dir, request.FILES['attachment-file'], profile )
                
                attachment_name = post_data['attachment-name']
                if attachment_name is None or attachment_name == '':
                    attachment_name = request.FILES['attachment-file'].name
                
                attachment_url = settings.MEDIA_URL + "attachments/%s/%s" % ( profile.user.username, request.FILES['attachment-file'].name)
                attachment = ProfileAttachment( 
                                               profile = profile,
                                               name = attachment_name,
                                               url = attachment_url)
                
                attachment.save()
    
        # in case a link is posted instead of a file upload
        attachment_link = post_data['attachment-link']
        
        if attachment_link is not None and attachment_link != '':
            
            attachment_name = post_data['attachment-name']
            
            if attachment_name is None or attachment_name == '':
                attachment_name = attachment_link
            
            attachment = ProfileAttachment( 
                                           profile = profile,
                                           name = attachment_name,
                                           url = attachment_link)
            attachment.save()
                
    
    except:
        message = "Error saving profile"
        
        



    

    return {
            "profile": profile,
            "message": message,
            }


def save_file( request, target_dir, in_file, profile ):

    # saving it to temp first
    if not os.path.isdir( target_dir):
        os.makedirs( target_dir)
        
    out_file = target_dir + "/" + in_file.name
    with open( out_file, 'wb+' ) as destination:
        for chunk in in_file.chunks():
            destination.write( chunk )
    


def update_profile_data( post_data ):

    # check if this user exists
    message = ''

    # refreshing the data from AD
    user_data = LDAPBackend().populate_user( post_data['ldap-user-name'] )


    user_profile = Profile.objects.filter( user = user_data )
    if not user_profile:
        user_profile = Profile( user = user_data )
        user_profile.supervisor = user_profile.user
        message = 'New Profile'
    else:
        user_profile = user_profile[0]


    return {
            "user-profile": user_profile,
            "message": message,
            }

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

