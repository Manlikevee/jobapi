from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.generics import get_object_or_404
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
    usecases = messagestarter.objects.filter(Q(sender=user) | Q(reciever=user)).all()
    usecase = messagestarterserializer(usecases, many=True)
    jobcard = Jobs.objects.all().order_by('-id')[:7]
    jobserialized = Jobserializer(jobcard, many=True)
    jobcardcount = Jobs.objects.filter(likes__in=[user]).all().order_by('-id').count()
    # submitcount = Applications.objects.filter(user=request.user).count()

    context = {
        'usecase': usecase.data,
        'jobserialized': jobserialized.data,
        # 'submitcount':submitcount,
        'jobcardcount':jobcardcount,
        'allusers': allusers.data
    }

    return Response(context, status=status.HTTP_200_OK)






@permission_classes([IsAuthenticated])
@api_view(['GET'])
def userprofile(request):
    user = request.user
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



@permission_classes([IsAuthenticated])
@api_view(['GET'])
def usersaves(request):
    user = request.user
    jobcards = Jobs.objects.filter(likes__in=[user]).all().order_by('-id')
    jobcard = Jobserializer(jobcards, many=True)
    jobcardscount = Jobs.objects.filter(likes__in=[user]).all().count

    context = {
        'jobcard': jobcards.data,
        'jobcardscount': jobcardscount,
    }

    return Response(context, status=status.HTTP_200_OK)



def like_post(request):
    if request.method == 'POST':
        # Get the post ID from the POST data
        post_id = request.POST.get('post_id')

        # Retrieve the post object from the database
        try:
            post = Jobs.objects.get(id=post_id)
        except Jobs.DoesNotExist:
            return JsonResponse({'saved': False, 'message': 'Post not found'})

        # Check if the post is already saved by the current user
        if post.likes.filter(id=request.user.id).exists():
            # If yes, remove the current user from the post's saved_by ManyToMany field
            post.likes.remove(request.user)
            saved = False
            message = 'Post unsaved successfully'
        else:
            # If no, add the current user to the post's saved_by ManyToMany field
            post.likes.add(request.user)
            saved = True
            message = 'Post saved successfully'

        return JsonResponse({'saved': saved, 'message': message})

    # Return an error response for unsupported methods
    return JsonResponse({'saved': False, 'message': 'Invalid request method'})



def like_blog(request):
    if request.method == 'POST':
        # Get the post ID from the POST data
        post_id = request.POST.get('post_id')

        # Retrieve the post object from the database
        try:
            post = postings.objects.get(id=post_id)
        except postings.DoesNotExist:
            return JsonResponse({'saved': False, 'message': 'Post not found'})

        # Check if the post is already saved by the current user
        if post.likes.filter(id=request.user.id).exists():
            # If yes, remove the current user from the post's saved_by ManyToMany field
            post.likes.remove(request.user)
            saved = False
            message = 'Post liked successfully'
            like_count = post.likes.count()
        else:
            # If no, add the current user to the post's saved_by ManyToMany field
            post.likes.add(request.user)
            saved = True
            message = 'Post unliked successfully'
            like_count = post.likes.count()

        return JsonResponse({'saved': saved, 'message': message, 'like_count': like_count})

    # Return an error response for unsupported methods
    return JsonResponse({'saved': False, 'message': 'Invalid request method'})






def unlike_post(request, id):
    post = get_object_or_404(Jobs, id=id)
    post.likes.remove(request.user)
    likes_count = post.likes.count()
    print('clicked')
    return JsonResponse({'likes': likes_count})



@permission_classes([IsAuthenticated])
@api_view(['GET'])
def userjobsdetail(request, id):
    jobdetails = get_object_or_404(Jobs, id=id)
    jobdetail =  Jobserializer(jobdetails)
    jobcard = Jobs.objects.all().exclude(id=jobdetails.id)[:4]
    jobcards = Jobserializer(jobcard, many=True)
    # user_publication_set = set(request.user.blogpost_like.values_list('id', flat=True))
    jds = jobfeatures.objects.filter(user=id)
    jd = Featuresserializer(jds)
    context = {
        # 'user_publication_set': user_publication_set,
        'jobdetail': jobdetail.data,
        'jobcards': jobcards.data,
        'jd': jd.data
    }

    return Response(context, status=status.HTTP_200_OK)


@permission_classes([IsAuthenticated])
@api_view(['POST'])
def keyword(request):
    userfirstname = request.user.first_name
    userlastname = request.user.first_name
    myuserprofile = 5
    if request.method == "POST":
        keyword = request.POST.get('keyword')
        keywordcount = Jobsalert.objects.filter(user=request.user).count()
        print(keywordcount)
        print(Jobsalert.objects.filter(user=request.user))
        account_users = Jobsalert.objects.filter(keyword=keyword).exists()
        if account_users:
            return Response({'message': 'This keyword already exists'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if keyword.is_valid:
                if keywordcount >= myuserprofile:
                    return Response({'message': 'You Have Exceeded Your Keyword Limit which is 5'}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    vee = Jobsalert.objects.create(user=request.user, keyword=keyword)
                    vee.save()
                    return Response({'message': 'Key Word Added Successfully'}, status=status.HTTP_200_OK)
    else:
        return Response({'message': 'We Are Unable To Process Your Request'}, status=status.HTTP_400_BAD_REQUEST)




@permission_classes([IsAuthenticated])
@login_required
@api_view(['GET'])
def usermessagecreate(request, id):
    myuser = get_object_or_404(User, id=id)
    print(myuser)
    s = shortuuid.ShortUUID(alphabet="0123456789")
    otp = s.random(length=15)
    messagemodel = messagestarter.objects.all()
    if messagestarter.objects.filter(Q(sender=request.user) | Q(reciever=request.user)).exists():

        if messagestarter.objects.filter(sender=request.user).filter(reciever=myuser).exists():
            allvee = messagestarter.objects.filter(sender=request.user).filter(reciever=myuser).first()
            message_id = allvee.messageid
            context = {
                # 'user_publication_set': user_publication_set,
                'id': message_id,
                'message': 'successfully fetched'
            }
            return Response(context, status=status.HTTP_200_OK)

        if messagestarter.objects.filter(sender=myuser).filter(reciever=request.user).exists():
            allvee = messagestarter.objects.filter(sender=myuser).filter(reciever=request.user).first()
            message_id = allvee.messageid
            context = {
                # 'user_publication_set': user_publication_set,
                'id': message_id,
                'message': 'successfully fetched'
            }
            return Response(context, status=status.HTTP_200_OK)
        else:
            messageobj = messagestarter(sender=request.user, reciever=myuser, messagetime=datetime.today(),
                                        messageid=otp)
            messageobj.save()

            messagestore = messagefolder.objects.update_or_create(messageid=messageobj.messageid,
                                                                  defaults={'messageid': messageobj})

            context = {
                # 'user_publication_set': user_publication_set,
                'id': messageobj.messageid,
                'message': 'Message Object Created'
            }
            return Response(context, status=status.HTTP_200_OK)

    else:

        messageobj = messagestarter(sender=request.user, reciever=myuser, messagetime=datetime.today(),
                                    messageid=otp)
        messageobj.save()

        messagestore = messagefolder.objects.update_or_create(messageid=messageobj.messageid,
                                                              defaults={'messageid': messageobj})

        context = {
            # 'user_publication_set': user_publication_set,
            'id': messageobj.messageid,
            'message': 'Message Object Created'
        }
        return Response(context, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def messageportal(request, id):
    messagetone = get_object_or_404(messagestarter, messageid=id)

    vee = datetime.now().date().strftime("%Y-%m-%d %H:%M:%S")
    if request.method == 'POST':
        keyword = request.data.get('keyword')
        print(keyword)
        if messagetone.sender == request.user:
            dest12 = {"sender": f"{request.user}", "reciever": f"{messagetone.reciever}", "messageid": f"{id}",
                      "messagetime": f"{vee}", "message": f"{keyword}"}
            jsondata = get_object_or_404(messagefolder, messageid=messagetone)
            jsondata.testj.append(dest12)
            jsondata.save()
            mymessage = messagefolder.objects.filter(messageid=messagetone).first()
            messageserialized = messageserializer(mymessage)

            apidata = {
                'messageserialized': messageserialized.data
            }

            return Response(apidata, status=status.HTTP_200_OK)
        if messagetone.reciever == request.user:
            dest12 = {"sender": f"{messagetone.reciever}", "reciever": f"{request.user}", "messageid": f"{id}",
                      "messagetime": f"{vee}", "message": f"{keyword}"}
            jsondata = get_object_or_404(messagefolder, messageid=messagetone)
            jsondata.testj.append(dest12)
            jsondata.save()
            mymessage = messagefolder.objects.filter(messageid=messagetone).first()
            messageserialized = messageserializer(mymessage)

            apidata = {
                'messageserialized': messageserialized.data
            }

            return Response(apidata, status=status.HTTP_200_OK)

    mymessage = messagefolder.objects.filter(messageid=messagetone).first()
    messageserialized = messageserializer(mymessage)


    apidata = {
        'messageserialized': messageserialized.data
    }

    return Response(apidata, status=status.HTTP_200_OK)
