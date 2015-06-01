from django.db import models
from django.db.models.fields.related import OneToOneField
from django.contrib.auth.models import User

# a profile of an Employee that HR holds
class Profile( models.Model ):

    user = OneToOneField( User, related_name = 'id_user_profile' )
    supervisor = models.ForeignKey( User )

    position = models.CharField( max_length = 64 )
    location = models.CharField( max_length = 64 )


    ROLES = {( '0-EMPL', 'Employee' ),
             ( '1-FMAN', 'Financial Manager' ),
             ( '2-OMAN', 'HR Manager' ), }

    role = models.CharField( max_length = 64,
                             choices = ROLES,
                             default = '0-EMPL' )

    SENIORITIES = {( '0-SEN', 'Senior Staff' ),
                   ( '1-MID', 'Middle Staff' ),
                   ( '2-STD', 'Staff' ),
                   ( '3-INT', 'Intern' ), }

    seniority = models.CharField( max_length = 64,
                                  choices = SENIORITIES,
                                  default = '2-STD' )


    workday_start = models.TimeField( default = "10:00" )
    workday_end = models.TimeField( default = "18:00" )



    leave_balance_HOLS = models.DecimalField( decimal_places = 2, max_digits = 4 )
    leave_balance_SICK = models.DecimalField( decimal_places = 2, max_digits = 4 )
    leave_balance_MATL = models.DecimalField( decimal_places = 2, max_digits = 4 )
    leave_balance_PATL = models.DecimalField( decimal_places = 2, max_digits = 4 )
    leave_balance_UNPD = models.DecimalField( decimal_places = 2, max_digits = 4 )

    leave_earn_HOLS = models.DecimalField( default = 2.0, decimal_places = 2, max_digits = 4 )
    leave_earn_SICK = models.DecimalField( default = 1.08, decimal_places = 2, max_digits = 4 )
