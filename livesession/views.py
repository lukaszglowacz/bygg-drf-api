from rest_framework import generics, status
from rest_framework.response import Response
from .models import LiveSession  # Importing the LiveSession model
from worksession.models import WorkSession  # Importing the WorkSession model for creating work logs
from .serializers import LiveSessionSerializer  # Importing the serializer for LiveSession
from django.utils import timezone  # Used to get the current date and time
from django.db import transaction  # For atomic database transactions
from rest_framework.permissions import IsAuthenticated  # Permission class to check if the user is authenticated

class StartLiveSessionView(generics.CreateAPIView):
    queryset = LiveSession.objects.all()  # Base queryset for all live sessions
    serializer_class = LiveSessionSerializer  # Serializer to handle LiveSession objects
    permission_classes = [IsAuthenticated]  # Ensures that only authenticated users can access this view

    def perform_create(self, serializer):
        # Custom method to define additional logic during the creation of a LiveSession
        serializer.save(status='Trwa')  # 'Trwa' means 'Ongoing' in Polish, setting the initial status of the session

class EndLiveSessionView(generics.UpdateAPIView):
    queryset = LiveSession.objects.all()  # Base queryset for all live sessions
    serializer_class = LiveSessionSerializer  # Serializer to handle LiveSession objects
    permission_classes = [IsAuthenticated]  # Ensures that only authenticated users can access this view

    def perform_update(self, serializer):
        with transaction.atomic():
            # Start of a database transaction to ensure data integrity
            session = serializer.instance
            session.end_time = timezone.now()  # Setting the end time of the session to the current time
            session.status = 'Zakończona'  # Changing the status to 'Zakończona' which means 'Ended' in Polish
            session.save()  # Save the changes to the session

            # Creating a corresponding WorkSession record using data from the ended LiveSession
            WorkSession.objects.create(
                profile=session.profile,
                workplace=session.workplace,
                start_time=session.start_time,
                end_time=session.end_time
            )
            session.delete()  # Deleting the LiveSession instance after transferring it to WorkSession

class ActiveLiveSessionsView(generics.ListAPIView):
    serializer_class = LiveSessionSerializer  # Serializer to handle LiveSession objects
    permission_classes = [IsAuthenticated]  # Ensures that only authenticated users can access this view

    def get_queryset(self):
        # Custom queryset method to filter the LiveSessions that are ongoing and belong to the logged-in user's profile
        profile = self.request.user.profile  # Accessing the user's profile associated with the request
        return LiveSession.objects.filter(status='Trwa', profile=profile).order_by('-start_time')
        # Filters LiveSessions that are ongoing ('Trwa') and belong to the user, ordered by start time in descending order
