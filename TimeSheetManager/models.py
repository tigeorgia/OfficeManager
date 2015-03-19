from django.db import models
from django.db.models.fields.related import OneToOneField, ManyToManyField
from django.contrib.auth.models import User
from django import forms



# Create your models here.


# the extension only includes the supervisor
class Employee( models.Model ):
    user = OneToOneField( User, related_name = 'id_user' )
    supervisor = models.ForeignKey( User )
    workday_start = models.TimeField( default = "10:00" )
    workday_end = models.TimeField( default = "18:00" )
    break_hours = models.IntegerField( default = 1 )
    location = models.CharField( max_length = 64 )
    position = models.CharField( max_length = 64 )
    ROLES = {( 'EMPL', 'Employee' ),
             ( 'FMAN', 'Financial Manager' ),
             ( 'OMAN', 'Office Manager' ), }
    role = models.CharField( max_length = 64,
                             choices = ROLES,
                             default = 'EMPL' )

    leave_balance_HOLS = models.DecimalField( decimal_places = 2, max_digits = 4)
    leave_balance_SICK = models.DecimalField( decimal_places = 2, max_digits = 4)
    leave_balance_MATL = models.DecimalField( decimal_places = 2, max_digits = 4)
    leave_balance_PATL = models.DecimalField( decimal_places = 2, max_digits = 4)
    leave_balance_UNPD = models.DecimalField( decimal_places = 2, max_digits = 4)

    leave_earn_HOLS = models.DecimalField( default = 2.0, decimal_places = 2, max_digits = 4 )
    leave_earn_SICK = models.DecimalField( default = 1.08, decimal_places = 2, max_digits = 4 )

# the data will be used in the calculation of the time sheet data
class Leave( models.Model ):
    start_date = models.DateField()
    end_date = models.DateField()
    employee = models.ForeignKey( Employee )
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



# is linked to user, date (month) and leaves related to the covered time period
class TimeSheet( models.Model ):
    employee = models.ForeignKey( Employee )
    leaves = ManyToManyField( Leave )
    # will use this to make sure time sheets are not repeated
    period = models.CharField( max_length = 64)
    # set to true by a financial manager
    salary_assigned = models.BooleanField( default = False )
    # set automatically
    submit_date = models.DateField()
    # set automatically, the data presence indicates it has been approved
    approve_date = models.DateField( null = True )
    # start_date
    start_date = models.DateField()
    end_date = models.DateField()
    approved_by = models.CharField( max_length = 64)
    
    # need to add the copy of these from employee to be able to report correctly
    # these here are final,after time sheet approval
    leave_balance_HOLS = models.DecimalField( decimal_places = 2, max_digits = 4, null = True  )
    leave_balance_SICK = models.DecimalField( decimal_places = 2, max_digits = 4, null = True  )
    leave_earn_HOLS = models.DecimalField( decimal_places = 2, max_digits = 4, null = True  )
    leave_earn_SICK = models.DecimalField( decimal_places = 2, max_digits = 4, null = True  )
    leave_used_HOLS = models.DecimalField( decimal_places = 2, max_digits = 4, null = True  )
    leave_used_SICK = models.DecimalField( decimal_places = 2, max_digits = 4, null = True  )
    

# salary Source
class SalarySource( models.Model ):
    code = models.CharField( max_length = 64 )
    
class SalarySourceForm( forms.ModelForm):
    class Meta:
        model = SalarySource
        fields = ['code']
        labels = {"code": "Add/Change Salary Code"}
        

# salary Assignment for a month
class SalaryAssignment( models.Model ):
    source = models.ForeignKey( SalarySource )
    employee = models.ForeignKey( Employee )
    period = models.CharField( max_length = 64)
    percentage = models.IntegerField()
