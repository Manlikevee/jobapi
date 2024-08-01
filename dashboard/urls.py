from django.urls import path, include

from users.views import upload_image, EmployeesAPIView, VisitorRequestAPIView, acceptvisitor, verifyvisitor, \
    getvisitordetails
from .views import *
from django.contrib.auth import views as auth_view
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

router = DefaultRouter()

urlpatterns = [

    path('chatdashboard', chatdashboard, name='chatdashboard'),
    path('userdashboarddata', jobseekerdashboard, name='jobseekerdashboard'),
    path('userprofile', userprofile, name='userprofile'),
    path('usersaves/', usersaves, name='usersaves'),
    path('like_post/', like_post, name='like_post'),
    path('savedlike_post/', savedlike_post, name='savedlike_post'),
    path('savedtimelinepost/', savedtimelinepost, name='savedtimelinepost'),
    path('unlike_post/', unlike_post, name='unlike_post'),
    path('userjobsdetail/', userjobsdetail, name='userjobsdetail'),
    path('keyword/', keyword, name='keyword'),
    path('newcomment/<int:id>/', newcomment, name='newcomment'),
    path('messageportal/<int:id>/', messageportals, name='messageportal'),
    path('usermessagecreate/<int:id>', usermessagecreate, name='usermessagecreate'),
    path('userjobs', userjobs, name='userjobs'),
    path('mupload_image/', upload_image, name='upload_image'),
    path('testcases/', testcases, name='testcases'),
    path('jobprint/', jobprint, name='jobprint'),
    path('userjobssinglepage/<int:id>/', userjobssinglepage, name='userjobssinglepage'),
    path('timetest', timetest, name='timetest'),
    path('userjobapplicationpage/<int:id>', user_job_application_page, name="userjobapplicationpage"),
    path('newtimelinepost', extract_hashtags, name="ExtractHashtagsView"),
    path('Timeline', Timeline, name="Timeline"),
    path('CommonTagAPIView', CommonTagAPIView.as_view(), name="CommonTagAPIView"),
    path('postingsinglepage/<int:id>', postingsinglepage, name="postingsinglepage"),
    path('applications/<int:pk>/', applications, name='applications'),
    path('tag/<slug:slug>/', tagged, name="tagged"),
    path('employee', EmployeesAPIView.as_view(), name='EmployeesAPIView'),
    path('visitor', VisitorRequestAPIView.as_view(), name='VisitorRequestAPIView'),
    path('phonesearch', SearchEmployeeByPhoneNumberAPIView.as_view(),
         name='search_employee_by_phone'),
    path('messagedashboard', messagedashboard, name='messagedashboard'),
    path('userqrcards', userqrcards, name='userqrcards'),
    path('acceptvisitor', acceptvisitor, name='acceptvisitor'),
    path('verifyvisitor', verifyvisitor, name='verifyvisitor'),
    path('getvisitordetails', getvisitordetails, name='getvisitordetails'),
    path('upload/', upload_image, name='upload_image'),
    path('deletemessageportals/<int:id>', deletemessageportals, name='deletemessageportals'),
    path('api/create-company/', create_company, name='create-company'),
    path('universities/', UniversityListCreateView.as_view(), name='university-list-create'),

]
