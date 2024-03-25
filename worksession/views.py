from django.db.models.functions import TruncMonth, TruncDay, ExtractWeek, ExtractYear
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from .models import WorkSession
from .serializers import WorkSessionSerializer
from drf_api.permissions import IsOwnerOrReadOnly, IsEmployer, IsEmployeeOrReadOnly
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .filters import WorkSessionFilter
from django.db.models import Sum, F
from rest_framework.views import APIView
from rest_framework.response import Response
from calendar import month_name
import datetime
from collections import defaultdict
from rest_framework import permissions

class MonthlyWorkSessionSummary(APIView):
    # Definiowanie klas uprawnień
    permission_classes = [permissions.IsAuthenticated, IsEmployer | IsEmployeeOrReadOnly]

    def get(self, request, *args, **kwargs):
        user = request.user
        base_query = WorkSession.objects.annotate(
            month=TruncMonth('start_time'),
            year=ExtractYear('start_time')
        )

        # Jeśli użytkownik nie jest pracodawcą, ogranicz wyniki do jego danych
        if not user.is_employer:
            base_query = base_query.filter(user=user)

        summary = base_query.values(
            'year', 'month', 'user__id',
            'user__profile__first_name', 'user__profile__last_name'
        ).annotate(
            total_hours=Sum('total_time')
        ).order_by('year', 'month', 'user__id')

        readable_summary = []
        for entry in summary:
            month_year = f"{month_name[entry['month'].month]} {entry['year']}"
            user_name = f"{entry['user__profile__first_name']} {entry['user__profile__last_name']}"
            readable_summary.append({
                'month_year': month_year,
                'user_id': entry['user__id'],
                'user_name': user_name,
                'total_hours': entry['total_hours']
            })

        return Response(readable_summary)

class WeeklyWorkSessionSummary(APIView):
    # Definiowanie klas uprawnień
    permission_classes = [permissions.IsAuthenticated, IsEmployer | IsEmployeeOrReadOnly]

    def get(self, request, *args, **kwargs):
        user = request.user
        base_query = WorkSession.objects.annotate(
            week=ExtractWeek('start_time'),
            year=ExtractYear('start_time')
        )

        # Filtracja danych na podstawie roli użytkownika
        if not user.is_employer:
            base_query = base_query.filter(user=user)

        summary = base_query.values(
            'year', 'week', 'user__id',
            'user__profile__first_name', 'user__profile__last_name'
        ).annotate(
            total_hours=Sum('total_time')
        ).order_by('year', 'week', 'user__id')

        readable_summary = []
        for entry in summary:
            user_name = f"{entry['user__profile__first_name']} {entry['user__profile__last_name']}"
            readable_summary.append({
                'year': entry['year'],
                'week': entry['week'],
                'user_id': entry['user__id'],
                'user_name': user_name,
                'total_hours': entry['total_hours']
            })

        return Response(readable_summary)

class DailyWorkSessionSummary(APIView):
    # Definiowanie klas uprawnień
    permission_classes = [permissions.IsAuthenticated, IsEmployer | IsEmployeeOrReadOnly]

    def get(self, request, *args, **kwargs):
        user = request.user
        requested_day_str = request.query_params.get('day', datetime.date.today().strftime('%Y-%m-%d'))
        requested_day = datetime.datetime.strptime(requested_day_str, '%Y-%m-%d').date()

        # Filtracja danych na podstawie roli użytkownika
        base_query = WorkSession.objects.filter(start_time__date=requested_day)
        if not user.is_employer:
            base_query = base_query.filter(user=user)

        sessions = base_query.order_by('user__id', 'workplace__id', 'start_time')

        user_summary = defaultdict(lambda: {'total_hours': 0, 'details': [], 'user_name': ''})

        for session in sessions:
            user_id = session.user_id
            user_summary[user_id]['user_name'] = f"{session.user.profile.first_name} {session.user.profile.last_name}"
            user_summary[user_id]['total_hours'] += session.total_time
            user_summary[user_id]['details'].append({
                'start_time': session.start_time.strftime('%H:%M'),
                'end_time': session.end_time.strftime('%H:%M'),
                'total_time': session.total_time,
                'workplace_address': f"{session.workplace.street} {session.workplace.street_number}, {session.workplace.postal_code} {session.workplace.city}",
                'workplace_id': session.workplace_id
            })

        # Przygotowanie i formatowanie danych do odpowiedzi
        response_data = []
        for user_id, data in user_summary.items():
            if user.is_employer or user_id == user.id:
                response_data.append({
                    'user_id': user_id,
                    'user_name': data['user_name'],
                    'day': requested_day_str,
                    'total_hours': data['total_hours'],
                    'time_slots': data['details']
                })

        return Response(response_data)

class WorkSessionPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class WorkSessionListCreateView(generics.ListCreateAPIView):
    serializer_class = WorkSessionSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = WorkSessionPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = WorkSessionFilter


    def get_queryset(self):
        # Teraz zwracamy wszystkie sesje pracy bez filtracji
        return WorkSession.objects.all()
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [IsOwnerOrReadOnly, IsEmployer]
        else:
            self.permission_classes = [IsOwnerOrReadOnly | IsEmployer]
        return super().get_permissions()

class WorkSessionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = WorkSession.objects.all()
    serializer_class = WorkSessionSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly | IsEmployer]

    def get_queryset(self):
        user = self.request.user
        queryset = WorkSession.objects.all()

        if not user.is_employer:
            queryset = queryset.filter(user=user)

        return queryset
