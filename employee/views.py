from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Employee
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView
from profiles.models import Profile
from .serializers import ProfileWithEmployeeSerializer

class EmployeeList(ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileWithEmployeeSerializer
    permission_classes = [IsAuthenticated]

class EmployeeDetail(RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = ProfileWithEmployeeSerializer
    permission_classes = [IsAuthenticated]
