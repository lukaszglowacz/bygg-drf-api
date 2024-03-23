from rest_framework import serializers
from .models import WorkSession

class WorkSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkSession
        fields = '__all__'