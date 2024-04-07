from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from profiles.views import UserRegistrationView
from profiles.serializers import MyTokenObtainPairView 



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('profile/', include('profiles.urls')),
    path('workplace/', include('workplace.urls')),
    path('worksession/', include('worksession.urls')),
    path('livesession/', include('livesession.urls')),
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', UserRegistrationView.as_view(), name='register'),
]
