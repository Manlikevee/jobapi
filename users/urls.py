from django.urls import path, include

from dashboard.views import alljobcards
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
    path('jobapprregister/', UserRegistrationView.as_view(), name='user-registration'),
    path('emailverification/', Useremailaccountverification.as_view(), name='user-Useremailaccountverification'),
    path('emailverification/verify/<str:auth_token>/', VerifyAccount.as_view(), name='verify-account'),
    path('newemailverification/verify/<str:auth_token>/<str:reference>/', VerifymyAccount.as_view(),
         name='newverify-account'),
    path('gac',  gemini_chat_completion_view,
         name='GroqChatCompletionView'),
    path('vvs', save_logos_for_instances,
         name='save_logos_for_instances'),
    path('alljobcards', alljobcards,
         name='alljobcards'),


]


