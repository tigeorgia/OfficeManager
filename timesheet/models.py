from django.db import models
from employee.models import Profile

# is linked to user, date (month) and leaves related to the covered time period
class TimeSheet( models.Model ):
    employee = models.ForeignKey( Profile )

    # will use this to make sure time sheets are not repeated
    period = models.CharField( max_length = 64)
    # boolean stating if salary has been assigned
    salary_assigned = models.BooleanField( default = False)
    
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
    leave_balance_before_HOLS = models.DecimalField( decimal_places = 2, max_digits = 4, null = True  )
    leave_balance_before_SICK = models.DecimalField( decimal_places = 2, max_digits = 4, null = True  )

    
    leave_balance_HOLS = models.DecimalField( decimal_places = 2, max_digits = 4, null = True  )
    leave_balance_SICK = models.DecimalField( decimal_places = 2, max_digits = 4, null = True  )
    leave_earn_HOLS = models.DecimalField( decimal_places = 2, max_digits = 4, null = True  )
    leave_earn_SICK = models.DecimalField( decimal_places = 2, max_digits = 4, null = True  )
    leave_used_HOLS = models.DecimalField( decimal_places = 2, max_digits = 4, null = True  )
    leave_used_SICK = models.DecimalField( decimal_places = 2, max_digits = 4, null = True  )
    
