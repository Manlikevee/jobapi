from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
# Create your views here.
from .models import Profile


def home(request):


    return render(request, 'index.html')


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email

        # ...
        try:
            profile = Profile.objects.get(user=user)
            token['is_updated'] = profile.profile_verified
            if not profile.is_verified:
                # Include accountnumber if the profile is not verified
                token['accountnumber'] = profile.accountnumber
        except Profile.DoesNotExist:
            pass  # Handle the case when the profile does not exist

        return token


class MyTokenObtainPairViews(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
