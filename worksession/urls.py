from django.urls import path
from .views import WorkSessionListCreateView, WorkSessionDetailView, MonthlyWorkSessionSummary, WeeklyWorkSessionSummary, DailyWorkSessionSummary

urlpatterns = [
    path('', WorkSessionListCreateView.as_view(), name='worksession-list'),
    path('<int:pk>/', WorkSessionDetailView.as_view(), name='worksession-detail'),
    path('monthly-summary/', MonthlyWorkSessionSummary.as_view(), name='monthly-summary'),
    path('weekly-summary/', WeeklyWorkSessionSummary.as_view(), name='weekly-summary'),
    path('daily-summary/', DailyWorkSessionSummary.as_view(), name='daily-summary'),
]