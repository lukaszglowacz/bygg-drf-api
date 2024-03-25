from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Profile
from .serializers import ProfileSerializer
from drf_api.permissions import IsOwnerOrReadOnly, IsEmployer
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from .serializers import UserRegistrationSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ProfileFilter

class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer


class ProfileList(ListCreateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProfileFilter

    def get_queryset(self):
        if self.request.user.is_employer:
            return Profile.objects.all()
        else:
            return Profile.objects.filter(user=self.request.user)

class ProfileDetail(RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly|IsEmployer]

    #Uzytkownik moze przegladac jedynie swoj profil
    def get_queryset(self):
        user = self.request.user
        return Profile.objects.filter(user=user)