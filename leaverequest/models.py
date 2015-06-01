from django.db import models
from employee.models import Profile
from django import forms

# the data will be used in the calculation of the time sheet data
class Leave( models.Model ):
    start_date = models.DateField()
    end_date = models.DateField()
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
    approved_by = models.CharField( max_length = 64)

# form to request a leave
class LeaveForm( forms.ModelForm ):
    class Meta:
        model = Leave
        fields = ['type', 'start_date', 'end_date', 'comment']
        labels = {"type": "Leave Type",
                  "start_date": "Start Date (YYYY-MM-DD)",
                  "end_date": "End Date (YYYY-MM-DD)",
                  "comment": "Comment (not required)"
                  }


