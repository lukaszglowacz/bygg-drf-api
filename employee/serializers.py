from rest_framework import serializers
from .models import Employee
from profiles.models import Profile

class EmployeeSerializer(serializers.ModelSerializer):
    profile = serializers.PrimaryKeyRelatedField(queryset=Profile.objects.all())

    class Meta:
        model = Employee
        fields = ['id', 'profile', 'total_hours_worked', 'current_work_location', 'work_start_time']
