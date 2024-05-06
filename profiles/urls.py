from django.urls import path
from . import views
from .views import ProfileWorkSessionsView

urlpatterns = [
    path('', views.ProfileList.as_view(), name='profile-list'),
    path('<int:pk>/', views.ProfileDetail.as_view(), name='profile-detail'),
    path('worksessions/', ProfileWorkSessionsView.as_view(), name='profile-work-sessions'),
]