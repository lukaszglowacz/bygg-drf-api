from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Employee
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView
from profiles.models import Profile
from .serializers import ProfileWithEmployeeSerializer
from django.utils.timezone import make_aware
import calendar
from django.utils.timezone import make_aware, datetime
from django.shortcuts import get_object_or_404
from drf_api.permissions import IsEmployer, IsEmployee

class EmployeeList(ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileWithEmployeeSerializer
    permission_classes = [IsEmployer]


from django.utils.timezone import make_aware, datetime
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from .serializers import ProfileWithEmployeeSerializer
from profiles.models import Profile
import calendar

class EmployeeDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = ProfileWithEmployeeSerializer
    permission_classes = [IsEmployer]

    def get_queryset(self):
        profile_id = self.kwargs.get('pk')
        year = self.request.query_params.get('year')
        month = self.request.query_params.get('month')

        if year and month:
            year = int(year)
            month = int(month)
            last_day = calendar.monthrange(year, month)[1]  # Pobierz ostatni dzień miesiąca
            start_date = make_aware(datetime(year, month, 1))
            end_date = make_aware(datetime(year, month, last_day, 23, 59, 59))

            # Zwróć queryset z sesjami pracy tylko z danego miesiąca i roku
            return Profile.objects.filter(
                id=profile_id,
                worksession__start_time__gte=start_date,
                worksession__start_time__lte=end_date
            ).distinct()

        return Profile.objects.filter(id=profile_id)  # Fallback dla profilu bez dat

    def get_object(self):
        # Metoda get_object musi zwracać pojedynczy obiekt
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset)
        return obj
