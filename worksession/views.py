from rest_framework import generics
from .models import WorkSession
from .serializers import WorkSessionSerializer
from rest_framework.permissions import IsAuthenticated
from .filters import WorkSessionFilter
from django_filters.rest_framework import DjangoFilterBackend

class WorkSessionListView(generics.ListCreateAPIView):
    """
    API view to list all work sessions or create a new work session.
    Only authenticated users can access this view.
    Supports filtering to allow users to find specific work sessions.
    """
    queryset = WorkSession.objects.all()
    serializer_class = WorkSessionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = (DjangoFilterBackend,)  # Specifies that this view uses the DjangoFilterBackend
    filterset_class = WorkSessionFilter  # Assigns the custom filter class that handles the filtering of work sessions
    
    def get_queryset(self):
        """
        Customizes the queryset to return work sessions ordered by start_time from newest to oldest.
        """
        return super().get_queryset().order_by('-start_time')  # Enhance readability by calling super()

class WorkSessionDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view that provides retrieve, update, and delete functionality for a specific work session.
    Selects related 'profile' and 'workplace' to optimize database access on retrieval.
    """
    queryset = WorkSession.objects.all().select_related('profile', 'workplace')  # Optimizes queries by prefetching related data
    serializer_class = WorkSessionSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        """
        Custom update logic to handle changes specifically to profile and workplace fields.
        This method will update the profile and workplace based on passed ID parameters and save the changes.
        """
        profile_id = self.request.data.get('profile_id')
        workplace_id = self.request.data.get('workplace_id')
        # Checking if profile_id or workplace_id is provided and updating the instance accordingly
        if profile_id:
            serializer.instance.profile_id = profile_id
        if workplace_id:
            serializer.instance.workplace_id = workplace_id
        serializer.save()  # Saves the instance with the updated data
