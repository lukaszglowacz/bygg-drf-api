from django.urls import path
from .views import StartLiveSessionView, EndLiveSessionView, ActiveLiveSessionsView

urlpatterns = [
    path('start/', StartLiveSessionView.as_view(), name='start-live-session'),
    path('end/<int:pk>/', EndLiveSessionView.as_view(), name='end-live-session'),
    path('active/', ActiveLiveSessionsView.as_view(), name='active-live-sessions'),
]
