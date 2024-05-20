from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, CreateAPIView
from .models import Profile
from .serializers import ProfileSerializer, UserRegistrationSerializer
from worksession.serializers import WorkSessionSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from worksession.models import WorkSession

class UserRegistrationView(CreateAPIView):
    """
    API view for registering new users.
    Allows any visitor to create a new user account.
    """
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]  # Allows access to any user without authentication.

class ProfileList(ListCreateAPIView):
    """
    API view that lists all profiles associated with the authenticated user or allows creation of new profiles.
    """
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]  # Ensures only authenticated users can access this view.

    def get_queryset(self):
        # Filters the profiles to return only those associated with the currently authenticated user.
        return Profile.objects.filter(user=self.request.user)
        
class ProfileDetail(RetrieveUpdateDestroyAPIView):
    """
    API view that provides retrieve, update, and destroy operations for a single profile.
    Only accessible to the authenticated user associated with the profile.
    """
    queryset = Profile.objects.all()  # Starts with a queryset of all profiles.
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]  # Ensures only authenticated users can access this view.

    def get_queryset(self):
        # Limits the profiles to those associated with the currently authenticated user.
        return Profile.objects.filter(user=self.request.user)
    
class ProfileWorkSessionsView(ListAPIView):
    """
    API view to list all work sessions associated with the profile of the authenticated user.
    """
    serializer_class = WorkSessionSerializer
    permission_classes = [IsAuthenticated]  # Ensures only authenticated users can access this view.

    def get_queryset(self):
        # Retrieves the profile associated with the logged-in user or returns a 404 if not found.
        user_profile = get_object_or_404(Profile, user=self.request.user)
        # Filters and returns work sessions related to the retrieved user profile.
        return WorkSession.objects.filter(profile=user_profile)
