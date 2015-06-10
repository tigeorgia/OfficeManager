from django.db import models
from employee.models import Profile
from django import forms

# the data will be used in the calculation of the time sheet data
class Leave( models.Model ):
    start_date = models.DateField()
    end_date = models.DateField()

    start_hour = models.TimeField( null = True )
    end_hour = models.TimeField( null = True )

    employee = models.ForeignKey( Profile )
    TYPES = {( 'HOLS', 'Vacation' ),
             ( 'SICK', 'Sick' ),
             ( 'MATL', 'M(P)aternity' ),
             ( 'OTHR', 'Other' ),
             ( 'UNPD', 'Unpaid Leave' )}

    type = models.CharField( max_length = 64,
                             choices = TYPES,
                             default = 'HOLS' )

    comment = models.TextField( blank = True, null = True )
    submit_date = models.DateField()
    approve_date = models.DateField( null = True )
    approved_by = models.CharField( max_length = 64 )
    workdays_requested = models.DecimalField( decimal_places = 2, max_digits = 5 )
    sick_balance = models.DecimalField( decimal_places = 2, max_digits = 5 )
    vacation_balance = models.DecimalField( decimal_places = 2, max_digits = 5 )
    declined = models.BooleanField( default = False )

# form to request a leave
class LeaveForm( forms.ModelForm ):
    class Meta:
        model = Leave
        fields = ['type', 'start_date', 'end_date', 'start_hour', 'end_hour', 'comment']
        labels = {"type": "Leave Type",
                  "start_date": "Start Date (YYYY-MM-DD)",
                  "end_date": "End Date (YYYY-MM-DD)",
                  "start_hour": "Start Hour (HH:mm)",
                  "end_hour": "End Hour (HH:mm)",

                  "comment": "Comment (not required)"
                  }
    def __init__( self, *args, **kwargs ):
        super( LeaveForm, self ).__init__( *args, **kwargs )
        self.fields['end_date'].required = False
        self.fields['start_hour'].required = False
        self.fields['end_hour'].required = False


