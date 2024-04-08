from rest_framework import serializers
from .models import LiveSession

class LiveSessionSerializer(serializers.ModelSerializer):
    user_first_name = serializers.CharField(source='user.profile.first_name', read_only=True)
    user_last_name = serializers.CharField(source='user.profile.last_name', read_only=True)
    workplace_detail = serializers.SerializerMethodField()

    class Meta:
        model = LiveSession
        fields = ['id', 'user', 'workplace', 'start_time', 'status', 'user_first_name', 'user_last_name', 'workplace_detail']

    def get_workplace_detail(self, obj):
        return f"{obj.workplace.street} {obj.workplace.street_number}, {obj.workplace.postal_code} {obj.workplace.city}"
