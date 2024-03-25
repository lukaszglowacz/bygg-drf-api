import django_filters
from .models import WorkSession
from django.db.models.functions import ExtractWeek

class WorkSessionFilter(django_filters.FilterSet):
    year = django_filters.NumberFilter(field_name='start_time', lookup_expr='year')
    month = django_filters.NumberFilter(field_name='start_time', lookup_expr='month')
    week = django_filters.NumberFilter(method='filter_by_week')
    day = django_filters.DateFilter(field_name='start_time', lookup_expr='date')
    workplace = django_filters.NumberFilter(method='filter_by_workplace_on_day')
    username = django_filters.CharFilter(field_name='user__id')

    class Meta:
        model = WorkSession
        fields = ['user_id', 'year', 'month', 'week', 'day', 'workplace']

    def filter_by_week(self, queryset, name, value):
        #Zakladajac, ze value to numer tygodnia
        return queryset.annotate(week=ExtractWeek('start_time')).filter(week=value)
    
    def filter_by_workplace_on_day(self, queryset, name, value):

        # Ta metoda filtruje sesje pracy przez miejsce pracy dla konkretnego dnia
        # Zakładając, że `value` to id miejsca pracy
        if 'day' in self.data:
            return queryset.filter(worplace_id=value)
        return queryset