from django.db import models

from employee.models import Profile

# salary Source
class SalarySource( models.Model ):
    code = models.CharField( max_length = 64 )

# class SalarySourceForm( forms.ModelForm):
#     class Meta:
#         model = SalarySource
#         fields = ['code']
#         labels = {"code": "Add/Change Salary Code"}



# salary Assignment for a month
class SalaryAssignment( models.Model ):
    source = models.ForeignKey( SalarySource )
    employee = models.ForeignKey( Profile )
    period = models.CharField( max_length = 64)
    percentage = models.IntegerField()


