from rest_framework import serializers
from .models import Profile, WorkSession, Workplace

class ProfileSerializer(serializers.ModelSerializer):
    total_work_hours = serializers.SerializerMethodField()
    workplaces_list = serializers.SerializerMethodField()
    user_email = serializers.SerializerMethodField()
    

    class Meta:
        model = Profile
        fields = ['id', 'total_work_hours', 'workplaces_list', 'first_name', 'last_name', 'personnummer', 'image', 'created_at', 'updated_at', 'user_email']

    def get_total_work_hours(self, obj):
        #Zwraca laczna ilosc przepracowanych godzin przez uzytkownika
        return obj.total_work_hours()
    
    def get_workplaces_list(self, obj):
        #Zwraca liste unikalnych miejsc, w ktorych przepracowal uzytkownik
        workplaces = obj.total_workplaces()
        return [f"{workplace.street} {workplace.street_number}, {workplace.postal_code} {workplace.city}" for workplace in workplaces]
    
    def get_user_email(self, obj):
        return obj.user.email