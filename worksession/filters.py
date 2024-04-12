from django_filters import rest_framework as filters
from .models import WorkSession, Profile

class WorkSessionFilter(filters.FilterSet):
    profile = filters.ModelChoiceFilter(queryset=Profile.objects.all())
    start_min = filters.DateTimeFilter(field_name="start_time", lookup_expr='gte')
    start_max = filters.DateTimeFilter(field_name="start_time", lookup_expr='lte')

    class Meta:
        model = WorkSession
        fields = ['profile', 'start_min', 'start_max']
