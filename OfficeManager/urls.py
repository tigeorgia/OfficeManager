from django.conf.urls import patterns, include, url
from django.contrib import admin
from frontpage.views import frontpage , sitelogout, front_page

from budgetshare.views import import_salary_assignments
from publicholidays.views import import_public_holidays
from timesheet.views import submit_time_sheet
from leaverequest.views import request_leave
from documentworkflow.views import list_requests_to_approve, approved_documents
from employee.views import manage_users, manage_profile

urlpatterns = patterns( '',
    url( r'^admin/', include( admin.site.urls ) ),
    url( r'^$', frontpage),
    url( r'^logout/$', sitelogout, name = "system-logout" ),
    #url( r'^timesheet/', include( 'TimeSheetManager.urls') ),
    url( r'^budgetshare/$', import_salary_assignments, name = "import-salary-assignments"),
    url( r'^publicholidays/$', import_public_holidays, name = "import-public-holidays"),
    
    
    url( r'^operations$', front_page, name = "time-sheet-front" ),
    url( r'^submittimesheet$', submit_time_sheet, name = "submit-time-sheet" ),
    url( r'^requestleave$', request_leave, name = "request-leave" ),
    url( r'^docstoapprove$', list_requests_to_approve, name = "documents-to-approve" ),
    #     url( r'^salarysources$', manage_salary_sources, name = "manage-salary-sources" ),
    #     url( r'^assignsalary$', assign_salary_sources, name = "assign-salary" ),
    url( r'^manageaccounts$', manage_users, name = "manage-accounts" ),
    url( r'^approveddocuments$', approved_documents, name = "approved-documents" ),
    
    url( r'^employeeprofile$', manage_profile, name = "employee-profile")


 )
