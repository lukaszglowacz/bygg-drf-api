from rest_framework import generics
from workplace.models import Workplace
from .serializers import WorkplaceSerializer
from drf_api.permissions import IsEmployer, ReadOnly
from django.http import JsonResponse

class WorkplaceListCreateView(generics.ListCreateAPIView):
    """
    This view handles listing all workplaces and creating new workplaces.
    Permissions are set to allow employers or read-only access.
    """
    queryset = Workplace.objects.all().order_by('street')  # Order workplaces by street name
    serializer_class = WorkplaceSerializer
    permission_classes = [IsEmployer | ReadOnly]  # Combines IsEmployer and ReadOnly permissions
    
    # Note: This method appears to be misplaced. It should be part of a separate view or handled within POST method logic.
    def workplace_view(request):
        """
        Handle the workplace-related requests. This method seems misplaced in a ListCreateAPIView
        and should either be part of another view handling POST requests or correctly integrated into this view.
        """
        if request.method == "POST":
            # Logic to handle a POST request. Should ideally be inside the post method of the view.
            return JsonResponse({"status": "success", "message": "Workplace added"})
        else:
            # Returning a JSON response for an invalid request method.
            return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)

class WorkplaceDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    This view handles the retrieval, updating, and deletion of individual workplace entries.
    Only users with employer status or read-only permissions can access these endpoints.
    """
    queryset = Workplace.objects.all()
    serializer_class = WorkplaceSerializer
    permission_classes = [IsEmployer | ReadOnly]  # Uses custom combined permissions for employer and read-only access.
