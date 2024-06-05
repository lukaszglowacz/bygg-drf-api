from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, CreateAPIView
from .models import Profile
from .serializers import ProfileSerializer, UserRegistrationSerializer
from worksession.serializers import WorkSessionSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from worksession.models import WorkSession

class UserRegistrationView(CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

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
        user_profile = get_object_or_404(Profile, user=self.request.user)
        return WorkSession.objects.filter(profile=user_profile)
