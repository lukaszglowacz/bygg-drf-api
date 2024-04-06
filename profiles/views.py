from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Profile
from .serializers import ProfileSerializer
from drf_api.permissions import IsEmployer, IsOwnerOrEmployer
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, permissions
from .serializers import UserRegistrationSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ProfileFilter

class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [ permissions.AllowAny ]


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
    permission_classes = [IsAuthenticated, IsOwnerOrEmployer]

    def get_queryset(self):
        user = self.request.user
        if user.is_employer:
            # Pracodawcy mają dostęp do wszystkich profili
            return Profile.objects.all()
        else:
            # Zwykli użytkownicy mogą zobaczyć tylko swój profil
            return Profile.objects.filter(user=user)
