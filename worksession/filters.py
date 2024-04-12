from django_filters import rest_framework as filters
from .models import WorkSession
from profiles.models import Profile
from workplace.models import Workplace
from django_filters import DateFilter

class WorkSessionFilter(filters.FilterSet):
    profile = filters.ModelChoiceFilter(queryset=Profile.objects.all(), label="Profile", to_field_name="id")
    workplace = filters.ModelChoiceFilter(queryset=Workplace.objects.all(), label="Workplace", to_field_name="id")
    start_min = DateFilter(field_name="start_time", lookup_expr='date__gte')
    start_max = DateFilter(field_name="start_time", lookup_expr='date__lte')

    class Meta:
        model = WorkSession
        fields = ['profile', 'workplace', 'start_min', 'start_max']
