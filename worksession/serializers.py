from rest_framework import serializers
from .models import WorkSession
from workplace.models import Workplace
from django.contrib.auth import get_user_model

User = get_user_model()

class WorkSessionSerializer(serializers.ModelSerializer):
    workplace = serializers.PrimaryKeyRelatedField(queryset=Workplace.objects.all())
    workplace_detail = serializers.SerializerMethodField(read_only=True)
    user_first_name = serializers.CharField(source='user.profile.first_name', read_only=True)
    user_last_name = serializers.CharField(source='user.profile.last_name', read_only=True)
    user_personnummer = serializers.CharField(source='user.profile.personnummer', read_only=True)

    # Ustawienie end_time jako opcjonalnego
    end_time = serializers.DateTimeField(allow_null=True, required=False)

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
    
    def create(self, validated_data):
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        # Aktualizacja instancji, w tym opcjonalne dodawanie end_time
        instance.end_time = validated_data.get('end_time', instance.end_time)
        
        # Nie jest konieczne ręczne obliczanie total_time, ponieważ jest to obsługiwane przez model
        instance.save()
        return instance