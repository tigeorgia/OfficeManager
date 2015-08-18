from django.db import models
from django import forms

class PublicHoliday( models.Model ):

    date = models.DateField()
    name = models.TextField( max_length = 256 )
    type = models.TextField( max_length = 256 )

    # entry mode,
    entry = models.TextField( max_length = 64, default = 'downloaded' )



class CustomHolidayForm( forms.ModelForm ):

    start_date = forms.DateField( label = "First day (YYYY-MM-DD)")
    end_date = forms.DateField( label = "Last day (YYYY-MM-DD)")
    name = forms.CharField( label = "Holiday name")

    class Meta:
        model = PublicHoliday
        fields = [ 'start_date', 'end_date', 'name']
