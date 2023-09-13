from django.conf import settings
from django.core import mail
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from rest_framework.generics import get_object_or_404
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

# from dashboard.serializer import Imagetest
# Create your views here.
from .models import Profile
from .serializer import *

def home(request):


    return render(request, 'index.html')

# login
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




class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)

        if serializer.is_valid():
            username = serializer.validated_data['username']
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            # Check if the username or email already exists
            if User.objects.filter(username=username).filter(email=email).exists():
                return Response({'message': 'User with Username and Email already exists'},
                                status=status.HTTP_400_BAD_REQUEST)

            if User.objects.filter(username=username).exists():
                return Response({'message': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
            if User.objects.filter(email=email).exists():
                return Response({'message': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)

            # Create the user
            user = serializer.save()
            j = get_object_or_404(Profile, user=user)
            auth_token = j.auth_token
            username = j.user.username
            useremail = j.user.email
            send_mail_after_registration(auth_token, username, useremail)
            return Response({'message': 'User registered successfully', 'accountnumber': user.profile.accountnumber},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Useremailaccountverification(APIView):
    def post(self, request):
        ref = request.data.get('reference')
        if ref is None:
            return Response({'message': 'Unable To Process Your Request'}, status=status.HTTP_400_BAD_REQUEST)

        j = get_object_or_404(Profile, accountnumber=ref)

        if j.is_verified:
            return Response({'message': 'Profile Already Verified'}, status=status.HTTP_400_BAD_REQUEST)

        if not j.is_verified:
            auth_token = j.auth_token
            username = j.user.username
            useremail = j.user.email
            print(f'email is {useremail}')
            myj = 'sjsj'
            # Attempt to send the email
            send_mail_after_registration(auth_token, username, useremail)

            payload = {'response': 'successfully sent confirmation email'}
            return Response(payload, status=status.HTTP_200_OK)

        return Response({'message': 'Unable To Process Your Request'}, status=status.HTTP_400_BAD_REQUEST)


def send_mail_after_registration(auth_token, username, useremail):
    print(useremail)
    subject = 'Your accounts need to be verified'
    lnk2 = 'https://veejobportal.netlify.app/'
    html_message = render_to_string('email-confirmation.html',
                                    {'token': auth_token, 'lnk2': lnk2, 'username': username})
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER
    to = [useremail]
    try:
        mail.send_mail(subject, plain_message, from_email, to, html_message=html_message)
        print('sending')
    except Exception as e:
        print(e)


class VerifyAccount(APIView):
    def get(self, request, auth_token):
        try:
            profile_obj = Profile.objects.filter(auth_token=auth_token).first()

            if profile_obj:
                if profile_obj.is_verified:
                    return Response({'error': 'Your account is already verified.'}, status=status.HTTP_200_OK)
                profile_obj.is_verified = True
                profile_obj.save()
                return Response({'message': 'Your account has been verified.'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid auth token.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': 'An error occurred.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VerifymyAccount(APIView):
    def get(self, request, auth_token, reference):
        try:
            profile_obj = Profile.objects.filter(auth_token=reference).filter(accountnumber=auth_token).first()

            if profile_obj:
                if profile_obj.is_verified:
                    return Response({'message': 'Your account is already verified.'}, status=status.HTTP_200_OK)
                profile_obj.is_verified = True
                profile_obj.save()
                return Response({'message': 'Your account has been verified.'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid auth token.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': 'An error occurred.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['POST'])
def upload_image(request):
    if request.method == 'POST':
        myimage = request.data.get('myimg')  # Assuming you're sending the image as 'myimg'
        print(myimage)
        serializer = UploadedImage.objects.create(image=myimage)
        if myimage:
            serializer.save()
            serializeddata = Imagetest(serializer)
            return Response(serializeddata.data, status=status.HTTP_201_CREATED)  # Use 201 Created status for successful resource creation
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)  # Return errors if the serializer is not valid
    else:
        return Response("Method not allowed", status=status.HTTP_405_METHOD_NOT_ALLOWED)
