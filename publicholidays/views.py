from django.shortcuts import render

import datetime
from employee.views import checkuserloggedin
from employee.models import Profile
import urllib
from BeautifulSoup import BeautifulSoup
from publicholidays.models import PublicHoliday

@checkuserloggedin
def import_public_holidays( request):
    
    employee = Profile.objects.get( user = request.user )
    
    DOWNLOAD_ADDRESS = "http://www.timeanddate.com/holidays/georgia/"
    
    current_year = datetime.date.today().year
    
    
    holidays = download_holidays( DOWNLOAD_ADDRESS, current_year)
    
    message = "Data has been downloaded from:\n\n%s%s" % ( DOWNLOAD_ADDRESS, current_year)
    
    return render( request, 
                   "import_public_holidays.html", 
                   { "employee": employee,
                     "message": message,
                     "holidays": holidays,
                     })

                  

def download_holidays( sourceurl, year):
    
    result = []
    
    htmldata = urllib.urlopen( sourceurl).read()
    
    soupdata = BeautifulSoup( htmldata).table
    
    rows = soupdata.findAll("tbody")[0].findAll("tr")
    
    for holiday in rows:
        date = holiday.find("th").contents
        
        holdata = holiday.findAll("td")
        
        holname = holdata[1].text
        holtype = holdata[2].text
        
        date = datetime.datetime.strptime("%s %s" % (date[0], year),
                                          "%b %d %Y")
        
        result.append(( date.strftime("%d %b %Y"), holname, holtype))
        
        holiday = PublicHoliday.objects.get_or_create( date = date, name = holname, type = holtype)
        
        
    return result