from django.urls import path
from .views import WorkSessionListCreateView, WorkSessionDetailView

urlpatterns = [
    path('', WorkSessionListCreateView.as_view(), name='worksession-list'),
    path('<int:pk>/', WorkSessionDetailView.as_view(), name='worksession-detail')
]