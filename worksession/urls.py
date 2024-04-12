from django.urls import path
from .views import WorkSessionListView, WorkSessionDetailView
urlpatterns = [
    path('', WorkSessionListView.as_view(), name='worksession-list'),
    path('<int:pk>/', WorkSessionDetailView.as_view(), name='worksession-detail'),
]