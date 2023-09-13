from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import *

class Userserializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']  # Or specify the fields you want to expose


class Completeprofile(serializers.ModelSerializer):
    user = Userserializer()

    class Meta:
        model = Profile
        fields = '__all__'  # Or specify the fields you want to expose

class Workexperienceserializer(serializers.ModelSerializer):
    class Meta:
        model = workexperience
        fields = '__all__'

class Universitydata(serializers.ModelSerializer):
    class Meta:
        model = exceltest
        fields = '__all__'

class Educationserializer(serializers.ModelSerializer):
    university = Universitydata()
    class Meta:
        model = University
        fields = '__all__'

class UserRegistrationSerializer(serializers.ModelSerializer):
    accountnumber = serializers.CharField(source='profile.accountnumber', read_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'accountnumber']
        extra_kwargs = {'password': {'write_only': True}}


class postingserializer(serializers.ModelSerializer):
    class Meta:
        model = postings
        fields = '__all__'