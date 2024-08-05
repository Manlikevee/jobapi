import json
import re
from urllib.request import urlretrieve

import requests
from django.conf import settings
from django.core import mail
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
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
import os
from groq import Groq
from dashboard.serializer import Imagetest
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
            print(password)
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
            user.save()
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
            return Response(serializeddata.data,
                            status=status.HTTP_201_CREATED)  # Use 201 Created status for successful resource creation
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)  # Return errors if the serializer is not valid
    else:
        return Response("Method not allowed", status=status.HTTP_405_METHOD_NOT_ALLOWED)


from rest_framework import status
from rest_framework.response import Response


class EmployeesAPIView(APIView):
    def get(self, request):
        # Retrieve all employees from the database
        employees_list = employees.objects.all()
        # Serialize the data
        serializer = EmployeesSerializer(employees_list, many=True)
        return Response(serializer.data)

    def post(self, request):
        # Deserialize the incoming data
        serializer = EmployeesSerializer(data=request.data)
        if serializer.is_valid():
            # Extract email and phone number from the request data
            email = serializer.validated_data.get('email')
            phone_number = serializer.validated_data.get('phone_number')

            # Check if an employee with the provided email or phone number already exists
            if employees.objects.filter(email=email).exists() or employees.objects.filter(
                    phone_number=phone_number).exists():
                return Response({"error": "Employee with provided email or phone number already exists."},
                                status=status.HTTP_400_BAD_REQUEST)

            # Save the data to the database
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VisitorRequestAPIView(APIView):
    def get(self, request):
        # Retrieve all visitor requests from the database
        visitor_requests = visitorslog.objects.all()
        # Serialize the data
        serializer = VisitorRequestSerializer(visitor_requests, many=True)
        return Response(serializer.data)

    def post(self, request):
        # Extract staff_id from the incoming data
        staff_id = request.data.get('staff_id')

        # Fetch the corresponding employee object
        try:
            employee = employees.objects.get(staff_id=staff_id)
        except employees.DoesNotExist:
            return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)

        # Get individual fields from the request data
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        email = request.data.get('email')
        phonenumber = request.data.get('phonenumber')
        reason = request.data.get('reason')
        visitation_type = request.data.get('visitation_type')

        # Create the visitor request
        visitor_request = visitorslog.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phonenumber=phonenumber,
            reason=reason,
            visitation_type=visitation_type,
            staff_id=employee
        )

        # Serialize the created visitor request
        serializer = VisitorRequestSerializer(visitor_request)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def acceptvisitor(request):
    if request.method == 'POST':
        # Get the post ID from the POST data
        visitor_id = request.data.get('post_id')

        # Retrieve the post object from the database
        try:
            post = visitorslog.objects.get(ref=visitor_id)
        except visitorslog.DoesNotExist:
            return JsonResponse({'message': 'Visitor not found'}, status=status.HTTP_404_NOT_FOUND)

        # Check if the post is already saved by the current user
        if post.status == 'awaiting_confirmation':
            post.status = 'pending_approval'
            post.save()
            message = 'Approval Successful'
        else:
            message = 'Already Confirmed'
        visitor_requests = visitorslog.objects.all()
        # Serialize the data
        serializer = VisitorRequestSerializer(visitor_requests, many=True)

        return Response({'message': message, 'visitorsdata': serializer.data}, status=status.HTTP_200_OK)

    # Return an error response for unsupported methods
    return JsonResponse({'message': 'Invalid request method'},
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
def verifyvisitor(request):
    if request.method == 'POST':
        # Get the post ID from the POST data
        visitor_id = request.data.get('post_id')
        tag_id = request.data.get('tag_id')

        try:
            post = visitorslog.objects.get(ref=visitor_id)
        except visitorslog.DoesNotExist:
            return JsonResponse({'message': 'Visitor not found'}, status=status.HTTP_404_NOT_FOUND)

        # Check if the post is already saved by the current user
        if post.status == 'awaiting_confirmation':
            post.status = 'pending_approval'
            post.save()
            message = 'Approval Successful'
        elif post.status == 'pending_approval':
            message = 'Unable To Complete Request'
            qrcodeobj = qrcodes.objects.filter(code_tag=tag_id).first()
            if not qrcodeobj:
                message = 'Tag Does Not Exist'
            elif qrcodeobj.availability == False:
                message = f'Tag Is Currently In Use and has not been logged out yet'
            elif qrcodeobj:
                post.tag_id = qrcodeobj.code_tag
                post.status = 'inprogress'
                post.save()
                qrcodeobj.availability = False
                qrcodeobj.used_by = post
                qrcodeobj.save()
                message = 'Proceed to visitation'
            else:
                message = 'Unable To Process Your Request'

        elif post.status == 'inprogress':
            message = 'Visitation Already In Progress, Kindly Proceed With Your Visitation'

        else:
            message = 'Invalid status'

        visitor_requests = visitorslog.objects.all()
        # Serialize the data
        serializer = VisitorRequestSerializer(visitor_requests, many=True)

        return Response({'message': message, 'visitorsdata': serializer.data}, status=status.HTTP_200_OK)

    # Return an error response for unsupported methods
    return JsonResponse({'message': 'Invalid request method'},
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
def getvisitordetails(request):
    if request.method == 'POST':
        visitor_id = request.data.get('post_id')
        # Retrieve the post object from the database
        try:
            post = visitorslog.objects.get(ref=visitor_id)
        except visitorslog.DoesNotExist:
            return JsonResponse({'message': 'Visitor not found'}, status=status.HTTP_404_NOT_FOUND)
        # Check if the post is already saved by the current user
        if post.status == 'awaiting_confirmation':
            message = 'Visitation Awaiting Confirmation'
        else:
            message = 'Visitation In Progress'
        # Serialize the data
        serializer = VisitorRequestSerializer(post)
        return Response({'message': message, 'visitorsdata': serializer.data}, status=status.HTTP_200_OK)
    # Return an error response for unsupported methods
    return JsonResponse({'message': 'Invalid request method'},
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
def logoutvisitor(request):
    if request.method == 'POST':
        # Get the post ID from the POST data
        visitor_id = request.data.get('post_id')
        tag_id = request.data.get('tag_id')

        if visitor_id:
            try:
                post = visitorslog.objects.get(ref=visitor_id)
                if post.status == 'Approval Successful':
                    post.status = 'visitation_complete'
                    post.save()
                    message = 'Visitation Complete'
                    tag = qrcodes.objects.filter(used_by=post).first()
                    tag.availability = True
                    tag.save()
                else:
                    message = 'Invalid request'

                visitor_requests = visitorslog.objects.all()
                # Serialize the data
                serializer = VisitorRequestSerializer(visitor_requests, many=True)

                return Response({'message': message, 'visitorsdata': serializer.data}, status=status.HTTP_200_OK)
            except visitorslog.DoesNotExist:
                return JsonResponse({'message': 'Visitor not found'}, status=status.HTTP_404_NOT_FOUND)

        elif tag_id:
            print('yoo')
        else:
            print('unable to process your request')

        try:
            post = visitorslog.objects.get(ref=visitor_id)
        except visitorslog.DoesNotExist:
            return JsonResponse({'message': 'Visitor not found'}, status=status.HTTP_404_NOT_FOUND)

    return JsonResponse({'message': 'Invalid request method'},
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)


import json
import re
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from groq import Groq  # Ensure you have the correct import for your Groq client


class GroqChatCompletionView(APIView):
    def post(self, request):
        try:
            client = Groq(
                api_key='',
            )

            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": "in json format write a job opening at board level for the company apple, write a very detailed description of the role, the salary range, the job title, the job service, and the job category also in json format, make sure the job description is long and detailed",
                    }
                ],
                model="llama3-8b-8192",
            )

            response_content = chat_completion.choices[0].message.content

            # Attempt to extract the JSON part from the response content
            json_str = None
            try:
                # Try to find the JSON object by looking for curly braces
                json_str = response_content[response_content.index('{'):response_content.rindex('}') + 1]
                job_data = json.loads(json_str)
            except (ValueError, json.JSONDecodeError) as e:
                return Response({
                    "error": "JSON format not found or is invalid in the response content",
                    "details": str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response(job_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def save_logos_for_instances(request):
    instances = exceltest.objects.filter(Q(schoollogo='') | Q(schoollogo=None)
                                         )
    print(instances)
    for instance in instances:
        try:
            # Fetch the image from the logourl
            result = urlretrieve(instance.logourl)
            instance.schoollogo.save(
                instance.logourl.split('/')[-1],  # Get the file name from the URL
                File(open(result[0], 'rb'))
            )
            instance.save()
            print(f"Saved logo for {instance.institution}")
        except Exception as e:
            print(f"Failed to fetch logo for {instance.institution}: {e}")

    return HttpResponse("Logos have been processed.")


