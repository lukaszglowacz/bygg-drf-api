from rest_framework import serializers
from .models import WorkSession
from workplace.models import Workplace

class WorkSessionSerializer(serializers.ModelSerializer):
    workplace = serializers.PrimaryKeyRelatedField(queryset=Workplace.objects.all())
    workplace_detail = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = WorkSession
        fields = ['id', 'user', 'workplace', 'workplace_detail', 'start_time', 'end_time', 'total_time']


    def get_workplace_detail(self, obj):
        workplace = obj.workplace
        return f"{workplace.street} {workplace.street_number}, {workplace.postal_code} {workplace.city}"
    
    def create(self, validated_data):
        return super().create(validated_data)