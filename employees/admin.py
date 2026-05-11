from django.contrib import admin
from .models import Employee

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('employee_name', 'email', 'role', 'department', 'status', 'joining_date')
    search_fields = ('employee_name', 'email', 'department')
    list_filter = ('status', 'department')
