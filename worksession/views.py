from rest_framework import generics
from .models import WorkSession
from .serializers import WorkSessionSerializer
from rest_framework.permissions import IsAuthenticated

class WorkSessionListView(generics.ListCreateAPIView):
    queryset = WorkSession.objects.all()
    serializer_class = WorkSessionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Sortuj wyniki od najnowszego do najstarszego według 'start_time'
        return WorkSession.objects.all().order_by('-start_time')

class WorkSessionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = WorkSession.objects.all()
    serializer_class = WorkSessionSerializer
    permission_classes = [IsAuthenticated]
