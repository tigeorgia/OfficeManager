from django.contrib import admin
from TimeSheetManager.models import Employee

# Only Employee model needs an admin site and that is for creating the first office manager,or should I do it from initiator code?
@admin.register( Employee)
class EmployeeAdmin( admin.ModelAdmin):
    list_display = ('user', 'role', 'supervisor')
    
    
