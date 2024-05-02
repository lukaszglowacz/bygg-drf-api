from rest_framework import serializers
from .models import Employee
from profiles.models import Profile


class ProfileWithEmployeeSerializer(serializers.ModelSerializer):
    employee_details = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['id', 'full_name', 'personnummer', 'employee_details']

    def get_employee_details(self, profile):
        employee = Employee.objects.filter(profile=profile).first()
        if employee:
            return {
                'total_hours_worked': employee.total_hours_worked,
                'current_work_location': employee.current_work_location,
                'work_start_time': employee.work_start_time,
            }
        return None