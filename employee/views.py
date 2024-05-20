from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Employee  # Importing Employee model, although not directly used in the views
from rest_framework.permissions import IsAuthenticated
from profiles.models import Profile  # Importing Profile model used in queries
from .serializers import ProfileWithEmployeeSerializer  # Importing the serializer for Profile
from django.utils.timezone import make_aware
import calendar
from django.utils.timezone import datetime  # Correcting import for datetime
from django.shortcuts import get_object_or_404
from drf_api.permissions import IsEmployer  # Custom permission class for employer restriction

class EmployeeList(ListCreateAPIView):
    queryset = Profile.objects.all()  # Queryset to include all profiles
    serializer_class = ProfileWithEmployeeSerializer  # Serializer to convert profile instances to JSON
    permission_classes = [IsEmployer]  # Restricts access to authenticated employers

class EmployeeDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = ProfileWithEmployeeSerializer  # Serializer for converting profile data
    permission_classes = [IsEmployer]  # Access restricted to employers

    def get_queryset(self):
        profile_id = self.kwargs.get('pk')  # Fetching the profile id from URL parameters
        year = self.request.query_params.get('year')  # Year parameter from URL query for filtering
        month = self.request.query_params.get('month')  # Month parameter from URL query for filtering

        if year and month:
            year = int(year)  # Converting year to integer
            month = int(month)  # Converting month to integer
            last_day = calendar.monthrange(year, month)[1]  # Fetching the last day of the specified month
            start_date = make_aware(datetime(year, month, 1))  # Creating a timezone aware datetime object for the start of the month
            end_date = make_aware(datetime(year, month, last_day, 23, 59, 59))  # and end of the month

            # Returns a queryset of profiles with work sessions that start within the specified month and year
            return Profile.objects.filter(
                id=profile_id,
                worksession__start_time__gte=start_date,
                worksession__start_time__lte=end_date
            ).distinct()

        # Default fallback to return a queryset for a profile with a specific id
        return Profile.objects.filter(id=profile_id)

    def get_object(self):
        # Overriding the default method to return the object based on the queryset
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset)  # Using Django's shortcut to get the object or return a 404 error
        return obj
