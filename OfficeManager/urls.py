from django.conf.urls import patterns, include, url
from django.contrib import admin
from frontpage.views import  sitelogout, front_page

from budgetshare.views import import_salary_assignments
from publicholidays.views import import_public_holidays, manage_custom_holidays
from timesheet.views import submit_time_sheet
from leaverequest.views import request_leave
from documentworkflow.views import list_requests_to_approve, approved_documents
from employee.views import manage_profile
from OfficeManager import settings
from django.views.generic.base import RedirectView
from django.core.urlresolvers import reverse_lazy
from documentrepository.views import publicdocuments

urlpatterns = patterns( '',
    url( r'^admin/', include( admin.site.urls ) ),
#     url( r'^$', frontpage),
#     url( r'^$', front_page, name = "front-page" ),
    url( r'^$', RedirectView.as_view( url = reverse_lazy( 'time-sheet-front' ) ), name = 'front-page' ),

    url( r'^logout/$', sitelogout, name = "system-logout" ),
    # url( r'^timesheet/', include( 'TimeSheetManager.urls') ),
    url( r'^budgetshare/$', import_salary_assignments, name = "import-salary-assignments" ),
    url( r'^publicholidays/$', import_public_holidays, name = "import-public-holidays" ),
    url( r'^customholidays/$', manage_custom_holidays, name = "manage-custom-holidays" ),


    url( r'^operations$', front_page, name = "time-sheet-front" ),
    url( r'^submittimesheet$', submit_time_sheet, name = "submit-time-sheet" ),
    url( r'^requestleave$', request_leave, name = "request-leave" ),
    url( r'^docstoapprove$', list_requests_to_approve, name = "documents-to-approve" ),
    #     url( r'^salarysources$', manage_salary_sources, name = "manage-salary-sources" ),
    #     url( r'^assignsalary$', assign_salary_sources, name = "assign-salary" ),
    #     url( r'^manageaccounts$', manage_users, name = "manage-accounts" ),
    url( r'^approveddocuments$', approved_documents, name = "approved-documents" ),

    url( r'^employeeprofile$', manage_profile, name = "employee-profile" ),
    
    url( r'^publicdocuments$', publicdocuments, name = "public-documents" ),
    

    # this is necessary for Django server to serve mediafiles, should be disabled when deployed to Apache
    url( r'^officemanager/media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT} ),


 )
