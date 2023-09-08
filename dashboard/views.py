from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializer import *
from users.models import *
from users.serializer import *
# Create your views here.




@permission_classes([IsAuthenticated])
@api_view(['GET'])
def jobseekerdashboard(request):
    user = request.user
    alluser = User.objects.exclude(id=10)
    allusers = Userserializer(alluser, many=True)
    # usecase = messagestarter.objects.filter(Q(sender=request.user) | Q(reciever=request.user)).all()
    jobcard = Jobs.objects.all().order_by('-id')[:7]
    jobserialized = Jobserializer(jobcard, many=True)
    jobcardcount = Jobs.objects.filter(likes__in=[user]).all().order_by('-id').count()
    # submitcount = Applications.objects.filter(user=request.user).count()

    context = {
        # 'usecase': usecase,
        'jobserialized': jobserialized.data,
        # 'submitcount':submitcount,
        'jobcardcount':jobcardcount,
        'allusers': allusers.data
    }

    return Response(context, status=status.HTTP_200_OK)






# @permission_classes([IsAuthenticated])
@api_view(['GET'])
def userprofile(request):
    user = User.objects.filter(id=10).first()
    user_profile = Profile.objects.filter(user=user).first()
    userprofile = Completeprofile(user_profile)
    workexpdata = workexperience.objects.filter(user=user).all()
    workexp = Workexperienceserialaizer(workexpdata, many=True)
    edudata = University.objects.filter(user=user).all()
    edu = Universityserialaizer(edudata, many=True)

    context = {
        'workexp': workexp.data,
        'edu': edu.data,
        'userprofile': userprofile.data
    }
    return Response(context, status=status.HTTP_200_OK)



# @permission_classes([IsAuthenticated])
@api_view(['GET'])
def usersaves(request):
    user = User.objects.filter(id=10).first()
    jobcards = Jobs.objects.filter(likes__in=[user]).all().order_by('-id')
    jobcard = Jobserializer(jobcards, many=True)
    jobcardscount = Jobs.objects.filter(likes__in=[user]).all().count

    context = {
        'jobcard': jobcard.data,
        'jobcardscount': jobcardscount,
    }

    return Response(context, status=status.HTTP_200_OK)