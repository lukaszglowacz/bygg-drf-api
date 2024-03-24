from django.db.models.functions import TruncMonth, TruncDay, ExtractWeek, ExtractYear
from rest_framework import generics
from .models import WorkSession
from .serializers import WorkSessionSerializer
from drf_api.permissions import IsOwnerOrReadOnly
from django.utils.dateparse import parse_date


class WorkSessionListCreateView(generics.ListCreateAPIView):
    serializer_class = WorkSessionSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        #Opcjonalnie umozliwia filtracje po miesiacu, tygodniu lub dniu
        queryset = WorkSession.objects.all()

        #Pobieranie parametrow zapytania
        year = self.request.query_params.get('year')
        month = self.request.query_params.get('month')
        week = self.request.query_params.get('week')
        day = self.request.query_params.get('day')

        #Filtracja po miesiacu
        if month:
            #Zakladajac, ze miesiac jest przekazywane w formacje YYYY-MM
            queryset = queryset.annotate(month=TruncMonth('start_time')).filter(month__month=month.split('-')[-1], month__year=month.split('-')[0])

        if week and year:
            queryset = queryset.annotate(week=ExtractWeek('start_time'), year=ExtractYear('start_time')).filter(week=week, year=year)

        if day:

            #Zakladajac, ze dzien przekazywany jest w formacie YYYY-MM-DD
            queryset = queryset.filter(start_time__date=day)
        
        #Uzytkownik widzi jedynie swoje sesje
        return queryset.filter(user=self.request.user)

class WorkSessionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = WorkSession.objects.all()
    serializer_class = WorkSessionSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        """
        Opcjonalnie: ogranicz zapytania tylko do profilu zalogowanego użytkownika.
        """
        user = self.request.user
        return WorkSession.objects.filter(user=user)