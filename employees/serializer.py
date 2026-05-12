from rest_framework import serializers
from .models import Employee

class EmployeeSerializer(serializers.ModelSerializer):
    def validate_email(self, value):
        return value or None

    def validate_phone(self, value):
        return value or None

    class Meta:
        model = Employee
        fields = '__all__'
