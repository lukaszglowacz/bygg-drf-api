from rest_framework import serializers
from .models import WorkSession
from workplace.models import Workplace
from django.contrib.auth import get_user_model

User = get_user_model()

class WorkSessionSerializer(serializers.ModelSerializer):
    workplace_detail = serializers.SerializerMethodField(read_only=True)
    user_first_name = serializers.CharField(source='user.profile.first_name', read_only=True)
    user_last_name = serializers.CharField(source='user.profile.last_name', read_only=True)
    user_personnummer = serializers.CharField(source='user.profile.personnummer', read_only=True)
    start_time = serializers.DateTimeField(format='%d.%m.%Y %H:%M', required=True, allow_null=False)
    end_time = serializers.DateTimeField(format='%d.%m.%Y %H:%M', allow_null=True, required=False)

    class Meta:
        model = WorkSession
        fields = [
            'id',
            'user',
            'user_first_name',
            'user_last_name',
            'user_personnummer',
            'workplace',
            'workplace_detail',
            'start_time',
            'end_time',
            'total_time'
        ]

    def get_workplace_detail(self, obj):
        workplace = obj.workplace
        return f"{workplace.street} {workplace.street_number}, {workplace.postal_code} {workplace.city}"
    
    def validate_workplace(self, value):
        if not value:
            raise serializers.ValidationError("Pole 'workplace' jest wymagane.")
    #    Sprawdzenie czy podane ID miejsca pracy istnieje w bazie danych
        if not Workplace.objects.filter(id=value).exists():
            raise serializers.ValidationError("Wybrane miejsce pracy nie istnieje.")
        return value

