from django.shortcuts import render
from django.http.response import HttpResponse

import datetime

def import_public_holidays( request):
    
    DOWNLOAD_ADDRESS = "http://www.timeanddate.com/holidays/georgia/"
    
    current_year = datetime.date.today().year
    
    return HttpResponse( 'Download public holidays from %s%d' % ( DOWNLOAD_ADDRESS, current_year))