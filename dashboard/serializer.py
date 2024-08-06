from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from users.models import *
from users.serializer import Userserializer
from taggit.serializers import (TagListSerializerField,
                                TaggitSerializer)


class companyserializer(serializers.ModelSerializer):

    class Meta:
        model = company
        fields = ['organization_name', 'logo', ]

class Jobserializer(serializers.ModelSerializer):
    organization = companyserializer()
    class Meta:
        model = Jobs
        fields = ['jobtitle','ref', 'jobservice', 'joblocation', 'jobcategory', 'jobsalaryrange', 'workinglevel', 'jobdescription', 'responsibilities', 'requirements', 'organization']  # Or specify the fields you want to expose




class seoserializer(serializers.ModelSerializer):

    class Meta:
        model = Jobs
        fields = ['jobtitle', 'jobdescription']

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


class ProfileSerializer(serializers.ModelSerializer):
    user = Userserializer()

    class Meta:
        model = Profile
        fields = '__all__'


class QrcodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = qrcodes
        fields = '__all__'


class ChatProfileSerializer(serializers.ModelSerializer):
    user = Userserializer()

    class Meta:
        model = Profile
        fields = ['avatar', 'bio', 'gender', 'last_seen', 'phonenumber', 'middle_name', 'user']


class messagestarterserializer(serializers.ModelSerializer):
    sender = Userserializer()
    reciever = Userserializer()
    sender_profile = ProfileSerializer(source='sender.profile', read_only=True)
    receiver_profile = ProfileSerializer(source='reciever.profile', read_only=True)

    class Meta:
        model = messagestarter
        fields = '__all__'


class chatmessagestarterserializer(serializers.ModelSerializer):
    sender = Userserializer()
    reciever = Userserializer()
    sender_profile = ChatProfileSerializer(source='sender.profile', read_only=True)
    receiver_profile = ChatProfileSerializer(source='reciever.profile', read_only=True)

    class Meta:
        model = messagestarter
        fields = '__all__'


class messageserializer(serializers.ModelSerializer):
    messageid = messagestarterserializer()

    class Meta:
        model = messagefolder
        fields = ['testj', 'lastupdated', 'messageid']


class chatmessageserializer(serializers.ModelSerializer):
    messageid = chatmessagestarterserializer()

    class Meta:
        model = messagefolder
        fields = ['testj', 'lastupdated', 'messageid']


class Imagetest(serializers.ModelSerializer):
    class Meta:
        model = UploadedImage
        fields = ['image']

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('id', 'image')
class postingserializer(serializers.ModelSerializer):
    user = Userserializer()
    sender_profile = ProfileSerializer(source='user.profile', read_only=True)

    class Meta:
        model = postings
        fields = '__all__'


class tagspostingserializer(TaggitSerializer, serializers.ModelSerializer):
    user = Userserializer()
    tags = TagListSerializerField()
    sender_profile = ProfileSerializer(source='user.profile', read_only=True)

    class Meta:
        model = postings
        fields = '__all__'
