from django.urls import path, include

from users.views import upload_image
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
    path('usersaves', usersaves, name='usersaves'),
    path('like_post', like_post, name='like_post'),
    path('unlike_post', unlike_post, name='unlike_post'),
    path('userjobsdetail', userjobsdetail, name='userjobsdetail'),
    path('keyword', keyword, name='keyword'),
    path('messageportal/<int:id>/', messageportal, name='messageportal'),
    path('usermessagecreate/<int:id>', usermessagecreate, name='usermessagecreate'),
    path('userjobs', userjobs, name='userjobs'),
    path('mupload_image/', upload_image, name='upload_image'),




]


