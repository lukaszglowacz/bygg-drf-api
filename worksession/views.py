from django.db.models.functions import TruncMonth, ExtractWeek, ExtractYear
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from .models import WorkSession
from .serializers import WorkSessionSerializer
from drf_api.permissions import IsOwnerOrReadOnly, IsEmployer
from rest_framework.permissions import IsAuthenticated

class WorkSessionPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class WorkSessionListCreateView(generics.ListCreateAPIView):
    serializer_class = WorkSessionSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = WorkSessionPagination

    def get_queryset(self):
        user = self.request.user
        queryset = WorkSession.objects.all()

        if not user.is_employer:
            queryset = queryset.filter(user=user)

        # Pobieranie parametrów zapytania
        year = self.request.query_params.get('year')
        month = self.request.query_params.get('month')
        week = self.request.query_params.get('week')
        day = self.request.query_params.get('day')
        username = self.request.query_params.get('username')

        #Filtracja po uzytkowniku
        if username:
            queryset = queryset.filter(user__username=username)

        # Filtracja po miesiącu
        if month:
            queryset = queryset.annotate(month=TruncMonth('start_time')).filter(
                month__month=month.split('-')[-1], month__year=month.split('-')[0])

        # Filtracja po tygodniu i roku
        if week and year:
            queryset = queryset.annotate(week=ExtractWeek('start_time'), year=ExtractYear('start_time')).filter(
                week=week, year=year)

        # Filtracja po dniu
        if day:
            queryset = queryset.filter(start_time__date=day)

        return queryset

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
