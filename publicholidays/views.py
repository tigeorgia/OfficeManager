from django.shortcuts import render

import datetime
from employee.views import checkuserloggedin
import urllib
from BeautifulSoup import BeautifulSoup
from publicholidays.models import PublicHoliday, CustomHolidayForm


@checkuserloggedin
def import_public_holidays( request, employee ):

    DOWNLOAD_ADDRESS = "http://www.timeanddate.com/holidays/georgia/"

    current_year = datetime.date.today().year


    holidays = download_holidays( DOWNLOAD_ADDRESS, current_year )

    message = "Data has been downloaded from:\n\n%s%s" % ( DOWNLOAD_ADDRESS, current_year )

    return render( request,
                   "import_public_holidays.html",
                   { "employee": employee,
                     "message": message,
                     "holidays": holidays,
                     } )



def download_holidays( sourceurl, year ):

    result = []

    htmldata = urllib.urlopen( sourceurl ).read()

    soupdata = BeautifulSoup( htmldata ).table

    rows = soupdata.findAll( "tbody" )[0].findAll( "tr" )

    for holiday in rows:
        date = holiday.find( "th" ).contents

        holdata = holiday.findAll( "td" )

        holname = holdata[1].text
        holtype = holdata[2].text

        date = datetime.datetime.strptime( "%s %s" % ( date[0], year ),
                                          "%b %d %Y" )

        result.append( ( date.strftime( "%d %b %Y" ), holname, holtype ) )

        holiday = PublicHoliday.objects.get_or_create( date = date, name = holname, type = holtype )


    return result




@checkuserloggedin
def manage_custom_holidays( request, employee ):

    defined_holidays = PublicHoliday.objects.filter( entry = "manual" ).order_by( "date")

    message = ''
    
    post_data = None
    
    if request.method == 'POST':
        
        if request.POST['button'] == 'Save':
            try:
                start_date = datetime.datetime.strptime( request.POST["start_date"], '%Y-%m-%d' ).date()
            except:
                message += "Please, define a correct start date<br>"
                
            try:
                end_date = datetime.datetime.strptime( request.POST["end_date"], '%Y-%m-%d' ).date()
            except:
                message += "Please, define a correct end date<br>"
            
            name =  request.POST["name"]
            if name == '':
                message += "Please define a name for the holiday<br>"
            
            hol_type = "public holiday"
            entry = "manual"
        
            if message == '':
                current = start_date + datetime.timedelta( days = -1)
                
                while True:
                    current += datetime.timedelta( days = 1)
                    holiday = PublicHoliday( 
                                            date = current,
                                            name = name,
                                            type = hol_type,
                                            entry = entry)
                    holiday.save()
                    if current == end_date:
                        break
            else:
                post_data = request.POST
                        
                
            
        if request.POST['button'] == 'Delete':
            holiday = PublicHoliday( id = request.POST['id'])
            holiday.delete()

    form = CustomHolidayForm( post_data)


    return render( request,
                   "manage_custom_holidays.html",
                   { 
                    "employee": employee,
                    "holidays": defined_holidays,
                    "form":form,
                    "message": message,
                     } )
