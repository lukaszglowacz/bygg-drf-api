from django.urls import path
from .views import DeleteUserView

urlpatterns = [
    # ... inne url patterns
    path('user/delete/', DeleteUserView.as_view(), name='user-delete'),
]
