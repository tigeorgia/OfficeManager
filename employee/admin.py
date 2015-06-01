from django.contrib import admin
from employee.models import Profile

@admin.register( Profile)
class EmployeeAdmin( admin.ModelAdmin):
    list_display = ('user', 'role', 'supervisor')
    
    
