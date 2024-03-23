from rest_framework import generics
from .models import WorkSession
from .serializers import WorkSessionSerializer

class WorkSessionListCreateView(generics.ListCreateAPIView):
    queryset = WorkSession.objects.all()
    serializer_class = WorkSessionSerializer

class WorkSessionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = WorkSession.objects.all()
    serializer_class = WorkSessionSerializer