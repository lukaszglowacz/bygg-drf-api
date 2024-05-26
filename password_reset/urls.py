from django.urls import path
from .views import PasswordResetView, PasswordResetConfirmView

urlpatterns = [
    path('', PasswordResetView.as_view(), name='password_reset'),
    path('confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]
