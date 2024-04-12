from django_filters import rest_framework as filters
from .models import WorkSession
from profiles.models import Profile
from workplace.models import Workplace

class WorkSessionFilter(filters.FilterSet):
    profile = filters.ModelChoiceFilter(queryset=Profile.objects.all(), label="Profile", to_field_name="id")
    workplace = filters.ModelChoiceFilter(queryset=Workplace.objects.all(), label="Workplace", to_field_name="id")

    class Meta:
        model = WorkSession
        fields = ['profile', 'workplace']
