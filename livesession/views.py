from rest_framework import generics, status
from rest_framework.response import Response
from .models import LiveSession
from worksession.models import WorkSession
from .serializers import LiveSessionSerializer
from django.utils import timezone
from django.db import transaction
from rest_framework.permissions import IsAuthenticated

class StartLiveSessionView(generics.CreateAPIView):
    queryset = LiveSession.objects.all()
    serializer_class = LiveSessionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(status='Trwa')

class EndLiveSessionView(generics.UpdateAPIView):
    queryset = LiveSession.objects.all()
    serializer_class = LiveSessionSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        with transaction.atomic():
            session = serializer.instance
            session.end_time = timezone.now()
            session.status = 'Zakończona'
            session.save()

            WorkSession.objects.create(
                profile=session.profile,  # używamy profile zamiast user
                workplace=session.workplace,
                start_time=session.start_time,
                end_time=session.end_time
            )
            session.delete()


class ActiveLiveSessionsView(generics.ListAPIView):
    serializer_class = LiveSessionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        profile = self.request.user.profile
        return LiveSession.objects.filter(status='Trwa', profile=profile).order_by('-start_time')

