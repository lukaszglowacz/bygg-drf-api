from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from .models import WorkSession
from .serializers import WorkSessionSerializer
from drf_api.permissions import IsEmployee, IsOwnerOrEmployer
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .filters import WorkSessionFilter
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.shortcuts import render
from django.core.serializers import serialize


class WorkSessionPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class WorkSessionListCreateView(generics.ListCreateAPIView):
    serializer_class = WorkSessionSerializer
    permission_classes = [IsOwnerOrEmployer]
    pagination_class = WorkSessionPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = WorkSessionFilter


    def get_queryset(self):
        if self.request.user.is_employer:
            return WorkSession.objects.all().order_by('-start_time')
        return WorkSession.objects.filter(user=self.request.user).order_by('-start_time')

    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if 'workplace' not in request.data:
            return Response({"error": "Workplace jest wymagany."}, status=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class WorkSessionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = WorkSession.objects.all()
    serializer_class = WorkSessionSerializer
    permission_classes = [IsOwnerOrEmployer]

    def get_object(self):
        obj = super().get_object()
        self.check_object_permissions(self.request, obj)
        return obj