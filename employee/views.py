from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Employee  # Importing Employee model, although not directly used in the views
from rest_framework.permissions import IsAuthenticated
from profiles.models import Profile  # Importing Profile model used in queries
from .serializers import ProfileWithEmployeeSerializer  # Importing the serializer for Profile
from django.utils.timezone import make_aware
import calendar
from django.shortcuts import get_object_or_404
from drf_api.permissions import IsEmployer  # Custom permission class for employer restriction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO
from django.http import HttpResponse
from django.utils.timezone import make_aware, datetime


from rest_framework.permissions import IsAuthenticated, AllowAny



from .models import Employee

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



import logging

logger = logging.getLogger(__name__)

class EmployeeMonthlySummaryPDF(APIView):
    permission_classes = [IsAuthenticated]

    def get_employee(self, employee_id):
        logger.debug(f"Attempting to get employee with id {employee_id}")
        try:
            employee = Employee.objects.get(profile__id=employee_id)
            logger.debug(f"Found employee: {employee}")
            return employee
        except Employee.DoesNotExist:
            logger.error(f"Employee with id {employee_id} not found")
            raise NotFound("Employee not found")

    def get(self, request, *args, **kwargs):
        employee_id = kwargs.get('id')
        logger.debug(f"Received request for monthly summary PDF for employee_id={employee_id}")
        year = int(request.query_params.get('year', datetime.now().year))
        month = int(request.query_params.get('month', datetime.now().month))
        logger.debug(f"Generating PDF for year={year}, month={month}")
        employee = self.get_employee(employee_id)
        logger.debug(f"Found employee: {employee}")

        start_date = make_aware(datetime(year, month, 1))
        last_day = calendar.monthrange(year, month)[1]
        end_date = make_aware(datetime(year, month, last_day, 23, 59, 59))

        sessions = employee.profile.worksession_set.filter(
            start_time__gte=start_date,
            start_time__lte=end_date
        )

        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4

        p.setFont("Helvetica", 12)
        p.drawString(100, height - 50, f"Monthly Summary for {employee.profile.full_name}")
        p.drawString(100, height - 70, f"Month: {calendar.month_name[month]}, {year}")
        p.drawString(100, height - 90, f"Email: {employee.profile.user.email}")

        y = height - 130
        for session in sessions:
            start = session.start_time.strftime('%Y-%m-%d %H:%M')
            end = session.end_time.strftime('%Y-%m-%d %H:%M')
            p.drawString(100, y, f"Workplace: {session.workplace.street} {session.workplace.street_number}, {session.workplace.city}")
            p.drawString(100, y - 20, f"Start: {start} - End: {end}")
            p.drawString(100, y - 40, f"Total Time: {session.total_time}")
            y -= 60
            if y < 60:
                p.showPage()
                y = height - 60

        p.showPage()
        p.save()

        buffer.seek(0)
        return HttpResponse(buffer, content_type='application/pdf')
