from rest_framework import serializers
from .models import Workplace

class WorkplaceSerializer(serializers.ModelSerializer):
    """
    Serializer for the Workplace model.
    
    This serializer automatically includes all fields from the Workplace model, making it convenient for creating
    and updating instances via API endpoints, and for fetching detailed information about workplaces.
    """
    class Meta:
        model = Workplace  # Specifies the model from which to construct the serializer.
        fields = '__all__'  # Includes every field from the Workplace model in the serializer.

