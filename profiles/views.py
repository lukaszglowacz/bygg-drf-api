from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Profile
from .serializers import ProfileSerializer

class ProfileList(ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

class ProfileDetail(RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer