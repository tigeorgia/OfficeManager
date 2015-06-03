from django.shortcuts import render
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt
from employee.views import checkuserloggedin
from employee.models import Profile




@checkuserloggedin
def frontpage( request, employee ):

    return render( request, 'frontpage.html', { "employee": employee, "hidemenu": True} )


def sitelogout( request ):
    logout( request )

    return render( request, 'frontpage.html')

# should present a few options to user/manager/etc.
# listing function filtered on the user role
@checkuserloggedin
@csrf_exempt
def front_page( request, employee ):

    return render( request, "time_sheet_front.html", {'employee': employee} )

# time sheet preview and submission


