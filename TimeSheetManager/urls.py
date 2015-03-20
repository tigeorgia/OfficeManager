from django.conf.urls import patterns, url
from TimeSheetManager import views

urlpatterns = patterns( '',
    url( r'^$', views.front_page, name = "time-sheet-front" ),
    url( r'^submittimesheet$', views.submit_time_sheet, name = "submit-time-sheet" ),
    url( r'^requestleave$', views.request_leave, name = "request-leave" ),
    url( r'^docstoapprove$', views.list_requests_to_approve, name = "documents-to-approve" ),
    url( r'^salarysources$', views.manage_salary_sources, name = "manage-salary-sources" ),
    url( r'^assignsalary$', views.assign_salary_sources, name = "assign-salary" ),
    url( r'^manageaccounts$', views.manage_users, name = "manage-accounts" ),
    url( r'^approveddocuments$', views.approved_documents, name = "approved-documents" ),


 )
