from rest_framework import generics
from .models import Workplace
from .serializers import WorkplaceSerializer

class WorkplaceListCreateView(generics.ListCreateAPIView):
    queryset = Workplace.objects.all()
    serializer_class = WorkplaceSerializer

class WorkplaceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Workplace.objects.all()
    serializer_class = WorkplaceSerializer