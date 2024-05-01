from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import *


class Userserializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'id']  # Or specify the fields you want to expose


class EmployeesSerializer(serializers.ModelSerializer):
    class Meta:
        model = employees
        fields = ['first_name', 'last_name', 'email', 'middle_name', 'phone_number', 'gender', 'staff_id' ]




class VisitorRequestSerializer(serializers.ModelSerializer):
    staff_id = EmployeesSerializer()

    class Meta:
        model = visitorslog
        fields = ['first_name', 'last_name', 'email', 'phonenumber', 'staff_id', 'reason', 'visitation_type', 'status', 'created_at', 'clock_in', 'clock_out', 'ref', 'reason', 'visitation_type', 'is_resheduled',  ]


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

    def create(self, validated_data):
        # Hash the password before saving
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)




