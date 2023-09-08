from django.urls import path, include

from .views import *
from django.contrib.auth import views as auth_view
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

router = DefaultRouter()




urlpatterns = [
    path('', home, name='home'),
    path('token/', MyTokenObtainPairViews.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='custom_token_refresh'),

]


