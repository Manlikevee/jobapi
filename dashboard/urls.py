from django.urls import path, include

from .views import *
from django.contrib.auth import views as auth_view
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

router = DefaultRouter()




urlpatterns = [
    path('userdashboarddata', jobseekerdashboard, name='jobseekerdashboard' ),
    path('userprofile', userprofile, name='userprofile' ),
    path('usersaves', usersaves, name='usersaves')
]


