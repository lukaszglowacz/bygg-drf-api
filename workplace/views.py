from rest_framework import generics
from .models import Workplace
from .serializers import WorkplaceSerializer
from drf_api.permissions import IsEmployee
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse

class WorkplaceListCreateView(generics.ListCreateAPIView):
    queryset = Workplace.objects.all().order_by('street') 
    serializer_class = WorkplaceSerializer
    permission_classes = [IsAuthenticated]
    

    def workplace_view(request):
        if request.method == "POST":
            # logika przetwarzania danych
            return JsonResponse({"status": "success", "message": "Workplace added"})
        else:
            return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)


class WorkplaceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Workplace.objects.all()
    serializer_class = WorkplaceSerializer
    permission_classes = [IsAuthenticated]