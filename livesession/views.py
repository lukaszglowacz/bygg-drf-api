from rest_framework import generics, status
from rest_framework.response import Response
from .models import LiveSession
from .serializers import LiveSessionSerializer
from django.utils import timezone
from worksession.models import WorkSession
from django.db import transaction
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone

class StartLiveSessionView(generics.CreateAPIView):
    queryset = LiveSession.objects.all()
    serializer_class = LiveSessionSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user, status='Trwa')
        
        
class EndLiveSessionView(generics.UpdateAPIView):
    queryset = LiveSession.objects.all()
    serializer_class = LiveSessionSerializer
    
    def perform_update(self, serializer):
        with transaction.atomic():
            session = serializer.instance
            session.end_time = timezone.now()
            session.status = 'Zakonczona'
            session.save()
        
            #Przeniesiemy rekord do Worksession
            WorkSession.objects.create(
                user = session.user,
                workplace = session.workplace,
                start_time = session.start_time,
                end_time = session.end_time
        )
        #Usun rekord z LiveSession
        session.delete()
        
class ActiveLiveSessionsView(generics.ListAPIView):
    serializer_class = LiveSessionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_employer:
            # Pracodawca widzi wszystkie aktywne sesje
            return LiveSession.objects.filter(status='Trwa').order_by('-start_time')
        else:
            # Pracownik widzi tylko swoje aktywne sesje
            return LiveSession.objects.filter(status='Trwa', user=user).order_by('-start_time')
    
    

