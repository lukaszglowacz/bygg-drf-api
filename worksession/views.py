from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from .models import WorkSession
from .serializers import WorkSessionSerializer
from drf_api.permissions import IsOwnerOrEmployer
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.shortcuts import render
from django.core.serializers import serialize
from django.core import serializers


class WorkSessionPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class WorkSessionListCreateView(generics.ListCreateAPIView):
    serializer_class = WorkSessionSerializer
    permission_classes = [IsOwnerOrEmployer]
    pagination_class = WorkSessionPagination
    


    def get_queryset(self):
        if self.request.user.is_employer:
            return WorkSession.objects.all().order_by('-start_time')
        return WorkSession.objects.filter(user=self.request.user).order_by('-start_time')

    
    def perform_create(self, serializer):
        if 'workplace' not in self.request.data:
            raise serializers.ValidationError({"error": "Workplace jest wymagany."})
        serializer.save(user=self.request.user)

        
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except serializers.ValidationError as e:
            return Response({"error": str(e.detail)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": "Wewnętrzny błąd serwera"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class WorkSessionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = WorkSession.objects.all()
    serializer_class = WorkSessionSerializer
    permission_classes = [IsOwnerOrEmployer]

    def get_object(self):
        obj = super().get_object()
        self.check_object_permissions(self.request, obj)
        return obj