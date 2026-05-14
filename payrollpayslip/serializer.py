from rest_framework import serializers
from .models import Payslip
from employees.serializer import EmployeeSerializer

class PayslipSerializer(serializers.ModelSerializer):
    employee_details = EmployeeSerializer(source='employee', read_only=True)
    
    class Meta:
        model = Payslip
        fields = '__all__'
        read_only_fields = ['created_at']
