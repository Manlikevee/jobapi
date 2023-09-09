from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from users.models import *
from users.serializer import Userserializer


class Jobserializer(serializers.ModelSerializer):
    class Meta:
        model = Jobs
        exclude = ['applied', 'payment_data', 'is_paidfor']  # Or specify the fields you want to expose


class Workexperienceserialaizer(serializers.ModelSerializer):
    class Meta:
        model = workexperience
        fields = '__all__'


class Unidata(serializers.ModelSerializer):
    class Meta:
        model = exceltest
        fields = '__all__'


class Universityserialaizer(serializers.ModelSerializer):
    university = Unidata()

    class Meta:
        model = University
        fields = '__all__'


class Featuresserializer(serializers.ModelSerializer):
    class Meta:
        model = jobfeatures
        fields = ['feature']




class messageserializer(serializers.ModelSerializer):
    messageid = messagestarter()
    class Meta:
        model = messagefolder
        fields = ['testj', 'lastupdated']


        
class messagestarterserializer(serializers.ModelSerializer):
    sender = Userserializer()
    reciever = Userserializer()
    message = messageserializer(source='messageid')
    class Meta:
        model = messagestarter
        fields = '__all__'
