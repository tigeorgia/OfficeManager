from django.db import models
from django.db.models.fields.related import OneToOneField
from django.contrib.auth.models import User


# a profile of an Employee that HR holds
class Profile( models.Model ):

    user = OneToOneField( User, related_name = 'id_user_profile' )
    supervisor = models.ForeignKey( User )

    position = models.CharField( max_length = 64 )

    LOCATIONS = {( '0-TBIL', 'Tbilisi' ),
                 ( '0-BATU', 'Batumi' ),
                 ( '0-KUTA', 'Kutaisi' ),
                 ( '0-ZUGD', 'Zugdidi' ),
                 }

    location = models.CharField( max_length = 64,
                                 choices = LOCATIONS,
                                 default = '0-TBIL' )


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



    # added using HR's list
    picture = models.ImageField( upload_to = 'profile', null = True )
    mobile_num = models.CharField( max_length = 256, null = True )
    personal_num = models.CharField( max_length = 256, null = True )

    date_of_birth = models.DateField( null = True )
    address = models.TextField( null = True )

    EMPLOYMENT_STATUS = {( '0-FULL', 'Full time' ),
                         ( '1-PART', 'Part time' )}

    employment_status = models.CharField( max_length = 64,
                                          choices = EMPLOYMENT_STATUS,
                                          default = '0-FULL',
                                          null = True )

    contract_start = models.DateField( null = True )
    contract_end = models.DateField( null = True )
    salary_gross_usd = models.DecimalField( decimal_places = 2, max_digits = 16, null = True )
    salary_net_usd = models.DecimalField( decimal_places = 2, max_digits = 16, null = True )

    # benefits
    insurance = models.BooleanField( default = False )
    gsm_limit = models.DecimalField( decimal_places = 2, max_digits = 16, default = '0.0' )











    # this will be moved to another model, somewhere in the timesheet application
    workday_start = models.TimeField( default = "10:00" )
    workday_end = models.TimeField( default = "18:00" )



    leave_balance_HOLS = models.DecimalField( decimal_places = 2, max_digits = 4 )
    leave_balance_SICK = models.DecimalField( decimal_places = 2, max_digits = 4 )
    leave_balance_MATL = models.DecimalField( decimal_places = 2, max_digits = 4, default = 0 )
    leave_balance_PATL = models.DecimalField( decimal_places = 2, max_digits = 4, default = 0 )
    leave_balance_UNPD = models.DecimalField( decimal_places = 2, max_digits = 4, default = 0 )

    #     # when a leave request is submitted these values will be held to updte balances correctly at the
    #     # time of timesheet submission
    #     leave_balance_HOLS_to_account_for = models.DecimalField( decimal_places = 2, max_digits = 4, default = 0 )
    #     leave_balance_SICK_to_account_for = models.DecimalField( decimal_places = 2, max_digits = 4, default = 0 )

    leave_earn_HOLS = models.DecimalField( default = 2.0, decimal_places = 2, max_digits = 4 )
    leave_earn_SICK = models.DecimalField( default = 1.08, decimal_places = 2, max_digits = 4 )





