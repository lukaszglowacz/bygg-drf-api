from django.urls import path
from .views import WorkplaceListCreateView, WorkplaceDetailView

urlpatterns = [
    path('', WorkplaceListCreateView.as_view(), name='workplace-list'),
    path('<int:pk>/', WorkplaceDetailView.as_view(), name='wokplace-detail'),
]