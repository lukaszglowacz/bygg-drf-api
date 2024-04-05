from rest_framework import generics
from .models import Workplace
from .serializers import WorkplaceSerializer
from drf_api.permissions import IsEmployer, IsEmployee, WorkPlacePermissions
from rest_framework.permissions import IsAuthenticated

class WorkplaceListCreateView(generics.ListCreateAPIView):
    queryset = Workplace.objects.all()
    serializer_class = WorkplaceSerializer
    permission_classes = [IsAuthenticated, WorkPlacePermissions]

class WorkplaceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Workplace.objects.all()
    serializer_class = WorkplaceSerializer
    permission_classes = [IsAuthenticated, WorkPlacePermissions]