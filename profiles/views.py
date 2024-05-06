from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Profile
from .serializers import ProfileSerializer
from drf_api.permissions import IsOwnerOrEmployer
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, permissions
from .serializers import UserRegistrationSerializer
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from worksession.models import WorkSession
from worksession.serializers import WorkSessionSerializer

class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [ permissions.AllowAny ]


class ProfileList(ListCreateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]


    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)
        

class ProfileDetail(RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)
    
class ProfileWorkSessionsView(ListAPIView):
    serializer_class = WorkSessionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Pobierz profil użytkownika na podstawie zalogowanego użytkownika
        user_profile = get_object_or_404(Profile, user=self.request.user)
        # Filtruj sesje pracy tylko dla tego profilu
        return WorkSession.objects.filter(profile=user_profile)