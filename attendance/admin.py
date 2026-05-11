from django.contrib import admin
from .models import Attendance

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('employee_name', 'status', 'intime', 'outtime')
    search_fields = ('employee_name', 'department')
    list_filter = ('status', 'department')
