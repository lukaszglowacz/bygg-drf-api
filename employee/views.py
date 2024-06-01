import logging
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from django.shortcuts import get_object_or_404
from django.utils.timezone import make_aware, datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
from django.http import HttpResponse
import calendar
from profiles.models import Profile
from .models import Employee
from .serializers import ProfileWithEmployeeSerializer
from drf_api.permissions import IsEmployer
from datetime import timedelta
import pytz

logger = logging.getLogger(__name__)

class EmployeeList(ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = ProfileWithEmployeeSerializer
    permission_classes = [IsEmployer]

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
            last_day = calendar.monthrange(year, month)[1]
            start_date = make_aware(datetime(year, month, 1))
            end_date = make_aware(datetime(year, month, last_day, 23, 59, 59))

            return Profile.objects.filter(
                id=profile_id,
                worksession__start_time__gte=start_date,
                worksession__start_time__lte=end_date
            ).distinct()

        return Profile.objects.filter(id=profile_id)

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset)
        return obj

class EmployeeMonthlySummaryPDF(APIView):
    permission_classes = [IsAuthenticated, IsEmployer]

    def get_employee(self, profile_id):
        logger.debug(f"Attempting to get employee with profile id {profile_id}")
        try:
            profile = Profile.objects.get(id=profile_id)
            employee = Employee.objects.get(profile=profile)
            logger.debug(f"Found employee: {employee}")
            return employee
        except Profile.DoesNotExist:
            logger.error(f"Profile with id {profile_id} not found")
            raise NotFound("Profile not found")
        except Employee.DoesNotExist:
            logger.error(f"Employee with profile id {profile_id} not found")
            raise NotFound("Employee not found")

    def split_sessions_by_day(self, sessions):
        split_sessions = []
        for session in sessions:
            start = session.start_time.astimezone(pytz.timezone("Europe/Stockholm"))
            end = session.end_time.astimezone(pytz.timezone("Europe/Stockholm"))
            current_start = start
            while current_start < end:
                session_end_of_day = current_start.replace(hour=23, minute=59, second=59, microsecond=999999)
                session_end = min(end, session_end_of_day)
                split_sessions.append({
                    "start_time": current_start,
                    "end_time": session_end,
                    "workplace": session.workplace,
                    "profile": session.profile
                })
                current_start = session_end + timedelta(seconds=1)
        return split_sessions

    def get(self, request, *args, **kwargs):
        profile_id = kwargs.get('id')
        logger.debug(f"Received request for monthly summary PDF for profile_id={profile_id}")
        if not profile_id:
            logger.error("Profile ID not provided")
            raise NotFound("Profile ID not provided")

        year = int(request.query_params.get('year', datetime.now().year))
        month = int(request.query_params.get('month', datetime.now().month))
        logger.debug(f"Generating PDF for year={year}, month={month}")

        employee = self.get_employee(profile_id)
        logger.debug(f"Found employee: {employee}")

        start_date = make_aware(datetime(year, month, 1))
        last_day = calendar.monthrange(year, month)[1]
        end_date = make_aware(datetime(year, month, last_day, 23, 59, 59))
        logger.debug(f"Filtering sessions between {start_date} and {end_date}")

        sessions = employee.profile.worksession_set.filter(
            start_time__gte=start_date,
            start_time__lte=end_date
        )

        split_sessions = self.split_sessions_by_day(sessions)
        days_in_month = [datetime(year, month, day).strftime('%Y-%m-%d') for day in range(1, last_day + 1)]

        sessions_by_day = {}
        for session in split_sessions:
            day = session["start_time"].strftime('%Y-%m-%d')
            if day not in sessions_by_day:
                sessions_by_day[day] = []
            sessions_by_day[day].append(session)

        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4,
                                rightMargin=0.5*inch, leftMargin=0.5*inch,
                                topMargin=0.5*inch, bottomMargin=0.5*inch)
        elements = []
        styles = getSampleStyleSheet()

        total_duration = sum(
            (session["end_time"] - session["start_time"]).total_seconds() for session in split_sessions
        )
        total_hours, remainder = divmod(total_duration, 3600)
        total_minutes = remainder // 60

        header_data = [
            [f"Monthly Summary for {employee.profile.full_name}"],
            [f"Personnummer: {employee.profile.personnummer}"],
            [f"Email: {employee.profile.user.email}"],
            [f"Month: {calendar.month_name[month]}, {year}"],
            [f"Total Hours Worked: {int(total_hours)} h, {int(total_minutes)} min"]
        ]
        header_table = Table(header_data, colWidths=[7.5 * inch])
        header_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 1), (-1, -1), 'MIDDLE'),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))

        elements.append(header_table)
        elements.append(Spacer(1, 12))

        session_data = [["Date", "Start Time", "End Time", "Workplace", "Total Hours"]]

        for day in days_in_month:
            if day in sessions_by_day:
                daily_total = sum((session["end_time"] - session["start_time"]).total_seconds() for session in sessions_by_day[day])
                daily_hours, daily_remainder = divmod(daily_total, 3600)
                daily_minutes = daily_remainder // 60

                first_entry = True
                for session in sessions_by_day[day]:
                    start_time = session["start_time"].strftime('%H:%M')
                    end_time = session["end_time"].strftime('%H:%M')
                    workplace = f"{session['workplace'].street} {session['workplace'].street_number}\n{session['workplace'].postal_code} {session['workplace'].city}"

                    if first_entry:
                        session_data.append([day, start_time, end_time, workplace, f"{int(daily_hours)} h, {int(daily_minutes)} min"])
                        first_entry = False
                    else:
                        session_data.append(["", start_time, end_time, workplace, ""])
            else:
                session_data.append([day, "No work", "", "", ""])

        session_table = Table(session_data, colWidths=[1.25 * inch, 1.25 * inch, 1.25 * inch, 2.75 * inch, 1.25 * inch])
        session_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 1), (-1, -1), 'MIDDLE'),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))

        elements.append(session_table)
        doc.build(elements)

        buffer.seek(0)
        return HttpResponse(buffer, content_type='application/pdf')
