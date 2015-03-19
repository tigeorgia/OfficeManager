from django.shortcuts import render
from TimeSheetManager.models import Employee
from django.contrib.auth import logout

def frontpage( request ):
    employee = None
    if request.user.is_authenticated():
        employee = Employee.objects.get( user = request.user )

    return render( request, 'frontpage.html', { "employee": employee, "hidemenu": True} )

def sitelogout( request ):
    logout( request )

    return render( request, 'frontpage.html')