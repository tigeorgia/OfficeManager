from django.conf.urls import patterns, include, url
from django.contrib import admin
from FrontPage.views import frontpage , sitelogout


urlpatterns = patterns( '',
    url( r'^admin/', include( admin.site.urls ) ),
    url( r'^$', frontpage ),
    url( r'^logout/$', sitelogout ),
    url( r'^timesheet/', include( 'TimeSheetManager.urls' ) )
 )
