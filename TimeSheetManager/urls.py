from django.conf.urls import patterns, url
from TimeSheetManager import views

urlpatterns = patterns('',
    url(r'^$', views.front_page),
    url(r'^submittimesheet$', views.submit_time_sheet),
    url(r'^requestleave$', views.request_leave),
    url(r'^docstoapprove$', views.list_requests_to_approve),
    url(r'^salarysources$', views.manage_salary_sources),
    url(r'^assignsalary$', views.assign_salary_sources),
    url(r'^manageaccounts$', views.manage_users),
    url(r'^approveddocuments$', views.approved_documents),
    
    
)
