from rest_framework import generics
from .models import WorkSession
from .serializers import WorkSessionSerializer
from rest_framework.permissions import IsAuthenticated
from .filters import WorkSessionFilter
from django_filters.rest_framework import DjangoFilterBackend

class WorkSessionListView(generics.ListCreateAPIView):
    queryset = WorkSession.objects.all()
    serializer_class = WorkSessionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = WorkSessionFilter
    
    
    def get_queryset(self):
        # Sortuj wyniki od najnowszego do najstarszego według 'start_time'
        return WorkSession.objects.all().order_by('-start_time')


class WorkSessionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = WorkSession.objects.all().select_related('profile', 'workplace')
    serializer_class = WorkSessionSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        """
        Custom update logic to handle only profile and workplace changes.
        """
        profile_id = self.request.data.get('profile_id')
        workplace_id = self.request.data.get('workplace_id')
        if profile_id:
            serializer.instance.profile_id = profile_id
        if workplace_id:
            serializer.instance.workplace_id = workplace_id
        serializer.save()

