import re
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.utils import timezone
from rest_framework import status, generics
from rest_framework.decorators import permission_classes, api_view, parser_classes
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from taggit.models import Tag

from .serializer import *
from users.models import *
from users.serializer import *
# Create your views here.
from faker import Faker

fake = Faker()


@api_view(['GET'])
def testcases(request):
    current_user = User.objects.filter(id=23).first()

    # Query messages where the current user is either the sender or receiver
    messages = messagestarter.objects.filter(
        Q(sender=current_user) | Q(reciever=current_user)
    )

    # Query messagefolder model for all message IDs in the selected messages
    all_messages_folders = messagefolder.objects.filter(messageid__in=messages).all()

    all_messages_folders_serializer = messageserializer(all_messages_folders, many=True)

    context = {
        'all_messages_folders': all_messages_folders_serializer.data,
    }

    return Response(context, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def jobseekerdashboard(request):
    current_time = timezone.now()
    Profile.objects.update_or_create(
        user=request.user,
        defaults={'last_seen': current_time}
    )
    user = request.user
    # Query messages where the current user is either the sender or receiver
    messages = messagestarter.objects.filter(
        Q(sender=user) | Q(reciever=user)
    )

    # Query messagefolder model for all message IDs in the selected messages
    all_messages_folders = messagefolder.objects.filter(messageid__in=messages).all().order_by('-lastupdated')
    all_messages_folders_serializer = messageserializer(all_messages_folders, many=True)
    alluser = User.objects.exclude(id=10)
    allusers = Userserializer(alluser, many=True)
    usecases = messagestarter.objects.filter(Q(sender=user) | Q(reciever=user)).all()
    usecase = messagestarterserializer(usecases, many=True)
    jobcard = Jobs.objects.all().order_by('-id')[:7]
    jobserialized = Jobserializer(jobcard, many=True)
    jobcardcount = Jobs.objects.filter(likes__in=[user]).all().order_by('-id').count()
    submitcount = Applications.objects.filter(user=request.user).count()

    context = {
        'usecase': usecase.data,
        'allmessages': all_messages_folders_serializer.data,
        'jobserialized': jobserialized.data,
        'submitcount': submitcount,
        'jobcardcount': jobcardcount,
        'allusers': allusers.data
    }

    return Response(context, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def chatdashboard(request):
    current_time = timezone.now()
    Profile.objects.update_or_create(
        user=request.user,
        defaults={'last_seen': current_time}
    )
    user = request.user
    # Query messages where the current user is either the sender or receiver
    messages = messagestarter.objects.filter(
        Q(sender=user) | Q(reciever=user)
    )

    # Query messagefolder model for all message IDs in the selected messages
    # all_messages_folders = messagefolder.objects.filter(messageid__in=messages).all().order_by('-lastupdated')
    # all_messages_folders_serializer = chatmessageserializer(all_messages_folders, many=True)
    # alluser = User.objects.exclude(id=request.user.id)
    # allusers = Userserializer(alluser, many=True)
    usecases = messagestarter.objects.filter(Q(sender=user) | Q(reciever=user)).all()
    usecase = chatmessagestarterserializer(usecases, many=True)
    allprofile = Profile.objects.exclude(user=request.user)
    allprofiles = ChatProfileSerializer(allprofile, many=True)

    context = {
        'usecase': usecase.data,
        # 'allmessages': all_messages_folders_serializer.data,
        # 'allusers': allusers.data,
        'allprofile': allprofiles.data
    }

    return Response(context, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def messagedashboard(request):
    current_time = timezone.now()
    Profile.objects.update_or_create(
        user=request.user,
        defaults={'last_seen': current_time}
    )
    user = request.user
    # Query messages where the current user is either the sender or receiver
    messages = messagestarter.objects.filter(
        Q(sender=user) | Q(reciever=user)
    )

    all_messages_folders = messagefolder.objects.filter(messageid__in=messages).all().order_by('-lastupdated')
    all_messages_folders_serializer = chatmessageserializer(all_messages_folders, many=True)
    context = {
        'allmessages': all_messages_folders_serializer.data,
    }

    return Response(context, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def userprofile(request):
    user = request.user
    current_time = timezone.now()
    user_profile = Profile.objects.filter(user=user).first()
    user_profile.last_seen = current_time
    user_profile.save()
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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def usersaves(request):
    user = request.user
    current_time = timezone.now()
    Profile.objects.update_or_create(
        user=request.user,
        defaults={'last_seen': current_time}
    )
    jobcards = Jobs.objects.filter(likes__in=[user]).all().order_by('-id')
    jobcard = Jobserializer(jobcards, many=True)

    context = {
        'jobcards': jobcard.data,
    }

    return Response(context, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def savedlike_post(request):
    if request.method == 'POST':
        # Get the post ID from the POST data
        post_id = request.data.get('post_id')

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
            user = request.user
            jobcards = Jobs.objects.filter(likes__in=[user]).all().order_by('-id')
            jobcard = Jobserializer(jobcards, many=True)

            context = {
                'jobcards': jobcard.data,
                'saved': saved,
                'message': message
            }

            return Response(context, status=status.HTTP_200_OK)
        else:
            # If no, add the current user to the post's saved_by ManyToMany field
            post.likes.add(request.user)
            saved = True
            message = 'Post saved successfully'
            user = request.user
            jobcards = Jobs.objects.filter(likes__in=[user]).all().order_by('-id')
            jobcard = Jobserializer(jobcards, many=True)

            context = {
                'jobcards': jobcard.data,
                'saved': saved,
                'message': message
            }

            return Response(context, status=status.HTTP_200_OK)

    # Return an error response for unsupported methods
    return JsonResponse({'saved': False, 'message': 'Invalid request method'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_post(request):
    if request.method == 'POST':
        # Get the post ID from the POST data
        post_id = request.data.get('post_id')

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
            jobcard = Jobs.objects.all().order_by('-id')
            jobserialized = Jobserializer(jobcard, many=True)

            context = {
                'jobcards': jobserialized.data,
                'saved': saved,
                'message': message
            }

            return Response(context, status=status.HTTP_200_OK)
        else:
            # If no, add the current user to the post's saved_by ManyToMany field
            post.likes.add(request.user)
            saved = True
            message = 'Post saved successfully'
            jobcard = Jobs.objects.all().order_by('-id')
            jobserialized = Jobserializer(jobcard, many=True)

            context = {
                'jobcards': jobserialized.data,
                'saved': saved,
                'message': message
            }

            return Response(context, status=status.HTTP_200_OK)

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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def userjobsdetail(request, id):
    current_time = timezone.now()
    Profile.objects.update_or_create(
        user=request.user,
        defaults={'last_seen': current_time}
    )
    user = request.user
    jobdetails = get_object_or_404(Jobs, id=id)
    jobdetail = Jobserializer(jobdetails)
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


@api_view(['POST'])
@permission_classes([IsAuthenticated])
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
                    return Response({'message': 'You Have Exceeded Your Keyword Limit which is 5'},
                                    status=status.HTTP_400_BAD_REQUEST)
                else:
                    vee = Jobsalert.objects.create(user=request.user, keyword=keyword)
                    vee.save()
                    return Response({'message': 'Key Word Added Successfully'}, status=status.HTTP_200_OK)
    else:
        return Response({'message': 'We Are Unable To Process Your Request'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def usermessagecreate(request, id):
    current_time = timezone.now()
    Profile.objects.update_or_create(
        user=request.user,
        defaults={'last_seen': current_time}
    )
    user = request.user
    myuser = get_object_or_404(User, id=id)
    print(myuser)
    s = shortuuid.ShortUUID(alphabet="0123456789")
    otp = s.random(length=15)
    messagemodel = messagestarter.objects.all()
    if messagestarter.objects.filter(Q(sender=request.user) | Q(reciever=request.user)).exists():

        if messagestarter.objects.filter(sender=request.user).filter(reciever=myuser).exists():
            allvee = messagestarter.objects.filter(sender=request.user).filter(reciever=myuser).first()
            message_id = allvee.messageid
            usecase = messagestarterserializer(allvee)
            context = {
                'usecase': usecase.data,
                'id': message_id,
                'message': 'successfully fetched'
            }
            return Response(context, status=status.HTTP_200_OK)

        if messagestarter.objects.filter(sender=myuser).filter(reciever=request.user).exists():
            allvee = messagestarter.objects.filter(sender=myuser).filter(reciever=request.user).first()
            message_id = allvee.messageid
            usecase = messagestarterserializer(allvee)
            context = {
                'usecase': usecase.data,
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

            usecase = messagestarterserializer(messageobj)
            context = {
                'usecase': usecase.data,
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

        usecase = messagestarterserializer(messageobj)
        context = {
            'usecase': usecase.data,
            'id': messageobj.messageid,
            'message': 'Message Object Created'
        }
        return Response(context, status=status.HTTP_200_OK)


@permission_classes([IsAuthenticated])
@api_view(['GET', 'POST'])
def messageportal(request, id):
    current_time = timezone.now()
    Profile.objects.update_or_create(
        user=request.user,
        defaults={'last_seen': current_time}
    )
    user = request.user
    # Query messages where the current user is either the sender or receiver
    messages = messagestarter.objects.filter(
        Q(sender=user) | Q(reciever=user)
    )

    # Query messagefolder model for all message IDs in the selected messages
    all_messages_folders = messagefolder.objects.filter(messageid__in=messages).all().order_by('-lastupdated')
    all_messages_folders_serializer = messageserializer(all_messages_folders, many=True)
    messagetone = get_object_or_404(messagestarter, messageid=id)
    messagetonedata = messagestarterserializer(messagetone)
    vee = timezone.now()
    if request.method == 'POST':
        myimage = request.data.get('myimg')
        keyword = request.data.get('keyword')
        print(keyword)
        if messagetone.sender == request.user:
            if myimage:
                serializer = UploadedImage.objects.create(image=myimage)
                serializer.save()
                serializeddata = Imagetest(serializer)
                dest12 = {"sender": f"{request.user}", "reciever": f"{messagetone.reciever}", "messageid": f"{id}",
                          "messagetime": f"{vee}", "message": f"{keyword}", "image": True,
                          "imageurl": serializeddata.data}
                jsondata = get_object_or_404(messagefolder, messageid=messagetone)
                jsondata.testj.append(dest12)
                jsondata.save()
                mymessage = messagefolder.objects.filter(messageid=messagetone).first()
                messageserialized = messageserializer(mymessage)

                apidata = {
                    'messageserialized': messageserialized.data,
                    'usersdataserialized': messagetonedata.data,
                    'allmessages': all_messages_folders_serializer.data
                }
                return Response(apidata, status=status.HTTP_200_OK)
            else:
                dest12 = {"sender": f"{request.user}", "reciever": f"{messagetone.reciever}", "messageid": f"{id}",
                          "messagetime": f"{vee}", "message": f"{keyword}", "image": False}
                jsondata = get_object_or_404(messagefolder, messageid=messagetone)
                jsondata.testj.append(dest12)
                jsondata.save()
                mymessage = messagefolder.objects.filter(messageid=messagetone).first()
                messageserialized = messageserializer(mymessage)

                apidata = {
                    'messageserialized': messageserialized.data,
                    'usersdataserialized': messagetonedata.data,
                    'allmessages': all_messages_folders_serializer.data
                }

                return Response(apidata, status=status.HTTP_200_OK)
        if messagetone.reciever == request.user:
            if myimage:
                serializer = UploadedImage.objects.create(image=myimage)
                serializer.save()
                serializeddata = Imagetest(serializer)
                dest12 = {"sender": f"{messagetone.reciever}", "reciever": f"{request.user}", "messageid": f"{id}",
                          "messagetime": f"{vee}", "message": f"{keyword}", "image": True,
                          "imageurl": serializeddata.data}
                jsondata = get_object_or_404(messagefolder, messageid=messagetone)
                jsondata.testj.append(dest12)
                jsondata.save()
                mymessage = messagefolder.objects.filter(messageid=messagetone).first()
                messageserialized = messageserializer(mymessage)

                apidata = {
                    'messageserialized': messageserialized.data,
                    'usersdataserialized': messagetonedata.data,
                    'allmessages': all_messages_folders_serializer.data
                }

                return Response(apidata, status=status.HTTP_200_OK)
            else:
                dest12 = {"sender": f"{messagetone.reciever}", "reciever": f"{request.user}", "messageid": f"{id}",
                          "messagetime": f"{vee}", "message": f"{keyword}", "image": False}
                jsondata = get_object_or_404(messagefolder, messageid=messagetone)
                jsondata.testj.append(dest12)
                jsondata.save()
                mymessage = messagefolder.objects.filter(messageid=messagetone).first()
                messageserialized = messageserializer(mymessage)

                apidata = {
                    'messageserialized': messageserialized.data,
                    'usersdataserialized': messagetonedata.data,
                    'allmessages': all_messages_folders_serializer.data
                }

                return Response(apidata, status=status.HTTP_200_OK)

    mymessage = messagefolder.objects.filter(messageid=messagetone).first()
    messageserialized = messageserializer(mymessage)

    apidata = {
        'messageserialized': messageserialized.data,
        'usersdataserialized': messagetonedata.data,
        'allmessages': all_messages_folders_serializer.data
    }

    return Response(apidata, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def messageportals(request, id):
    current_time = timezone.now()
    Profile.objects.update_or_create(
        user=request.user,
        defaults={'last_seen': current_time}
    )
    user = request.user
    # Query messages where the current user is either the sender or receiver
    messages = messagestarter.objects.filter(
        Q(sender=user) | Q(reciever=user)
    )

    # Query messagefolder model for all message IDs in the selected messages
    all_messages_folders = messagefolder.objects.filter(messageid__in=messages).all().order_by('-lastupdated')
    all_messages_folders_serializer = messageserializer(all_messages_folders, many=True)
    messagetone = get_object_or_404(messagestarter, messageid=id)
    print(messagetone)
    messagetonedata = messagestarterserializer(messagetone)
    vee = timezone.now()
    if request.method == 'POST':
        print('request', request.data)
        myimage = request.data.get('myimg')
        data = request.data.get('data')  # Assuming 'data' is the key containing the JSON payload
        image_data = request.FILES.get('myaudio')
        print('imafe is', myimage)
        print('data', data)
        if messagetone.sender == request.user:
            if image_data:
                serializerz = Image.objects.create(image=image_data)
                serializerz.save()
                serializer = ImageSerializer(serializerz).data

                data_dict = {}
                for key, value in request.data.items():
                    if 'myaudio' not in key:
                        field_name = key.split('[')[-1][:-1]  # Extract field name
                        data_dict[field_name] = value  # Assuming each key has only one value

                data_dict['datetime'] = str(vee)
                data_dict['senderid'] = request.user.id
                data_dict['recieverid'] = messagetone.reciever.id
                data_dict['audio_url'] = serializer['image']
                dest12 = data_dict
                jsondata = get_object_or_404(messagefolder, messageid=messagetone)
                jsondata.testj.append(dest12)
                jsondata.save()
                print('json obj', dest12)

                mymessage = messagefolder.objects.filter(messageid=messagetone).first()
                # print(mymessage)
                messageserialized = messageserializer(mymessage)

                apidata = {
                    'messageserialized': messageserialized.data,
                    'usersdataserialized': messagetonedata.data,
                    'allmessages': all_messages_folders_serializer.data
                }
                return Response(apidata, status=status.HTTP_200_OK)
            elif myimage:
                data_dict = {}
                for key, value in request.data.items():
                    if 'myimg' not in key:
                        field_name = key.split('[')[-1][:-1]  # Extract field name
                        data_dict[field_name] = value  # Assuming each key has only one value

                serializer = UploadedImage.objects.create(image=myimage)
                serializer.save()
                serializeddata = Imagetest(serializer).data
                print('serialized image', serializeddata)
                data_dict['datetime'] = str(vee)
                data_dict['senderid'] = request.user.id
                data_dict['recieverid'] = messagetone.reciever.id
                data_dict['imageUrl'] = serializeddata['image']
                dest12 = data_dict
                jsondata = get_object_or_404(messagefolder, messageid=messagetone)
                jsondata.testj.append(dest12)
                jsondata.save()
                print('json obj', dest12)

                mymessage = messagefolder.objects.filter(messageid=messagetone).first()
                # print(mymessage)
                messageserialized = messageserializer(mymessage)

                apidata = {
                    'messageserialized': messageserialized.data,
                    'usersdataserialized': messagetonedata.data,
                    'allmessages': all_messages_folders_serializer.data
                }
                return Response(apidata, status=status.HTTP_200_OK)
            else:

                # dest12 = {"sender": f"{request.user}", "reciever": f"{messagetone.reciever}", "messageid": f"{id}",
                #           "messagetime": f"{vee}", "image": False,
                #           "senderid": f"{request.user}",
                #           "receiverid": f"{messagetone.reciever}",
                #           "id": message_id,
                #           "type": message_type,
                #           "from": sender_from,
                #           "quotedid": quoted_message_id,
                #           "message": message_content,
                #           "datetime": f"{vee}",
                #
                #           }
                data['datetime'] = str(vee)
                data['senderid'] = request.user.id
                data['recieverid'] = messagetone.reciever.id

                dest12 = data
                print(data)
                print(str(request.user))
                jsondata = get_object_or_404(messagefolder, messageid=messagetone)
                jsondata.testj.append(dest12)
                jsondata.save()
                print('done', jsondata)
                mymessage = messagefolder.objects.filter(messageid=messagetone).first()
                messageserialized = messageserializer(mymessage)

                apidata = {
                    'messageserialized': messageserialized.data,
                    'usersdataserialized': messagetonedata.data,
                    'allmessages': all_messages_folders_serializer.data
                }

                return Response(apidata, status=status.HTTP_200_OK)
        if messagetone.reciever == request.user:
            if image_data:
                serializerz = Image.objects.create(image=image_data)
                serializerz.save()
                serializer = ImageSerializer(serializerz).data

                data_dict = {}
                for key, value in request.data.items():
                    if 'myaudio' not in key:
                        field_name = key.split('[')[-1][:-1]  # Extract field name
                        data_dict[field_name] = value  # Assuming each key has only one value









                data_dict['datetime'] = str(vee)
                data_dict['senderid'] = messagetone.reciever.id
                data_dict['recieverid'] = request.user.id
                data_dict['audio_url'] = serializer['image']
                dest12 = data_dict
                jsondata = get_object_or_404(messagefolder, messageid=messagetone)
                jsondata.testj.append(dest12)
                jsondata.save()
                print('json obj', dest12)

                mymessage = messagefolder.objects.filter(messageid=messagetone).first()
                # print(mymessage)
                messageserialized = messageserializer(mymessage)

                apidata = {
                    'messageserialized': messageserialized.data,
                    'usersdataserialized': messagetonedata.data,
                    'allmessages': all_messages_folders_serializer.data
                }
                return Response(apidata, status=status.HTTP_200_OK)

            elif myimage:
                data_dict = {}
                for key, value in request.data.items():
                    if 'myimg' not in key:
                        field_name = key.split('[')[-1][:-1]  # Extract field name
                        data_dict[field_name] = value  # Assuming each key has only one value

                serializer = UploadedImage.objects.create(image=myimage)
                serializer.save()
                serializeddata = Imagetest(serializer).data
                print('serialized image', serializeddata)
                jsondata = get_object_or_404(messagefolder, messageid=messagetone)
                # dest12 = {"sender": f"{messagetone.reciever}", "reciever": f"{request.user}", "messageid": f"{id}",
                #           "messagetime": f"{vee}", "message": f"{keyword}", "image": True,
                #           "imageurl": serializeddata.data,
                #
                #           "senderid": f"{messagetone.reciever}",
                #           "receiverid": f"{request.user}",
                #           "id": message_id,
                #           "type": message_type,
                #           "from": sender_from,
                #           "quotedid": quoted_message_id,
                #           "message": message_content,
                #           "datetime": f"{vee}",
                #           }
                # data['datetime'] = str(vee)
                # data['senderid'] =  messagetone.reciever.id
                # data['recieverid'] = request.user.id
                # data['imageUrl'] = serializeddata.data
                # dest12 = data
                data_dict['datetime'] = str(vee)
                data_dict['senderid'] = messagetone.reciever.id
                data_dict['recieverid'] = request.user.id
                data_dict['imageUrl'] = serializeddata['image']
                dest12 = data_dict
                jsondata.testj.append(dest12)

                jsondata.save()
                mymessage = messagefolder.objects.filter(messageid=messagetone).first()
                messageserialized = messageserializer(mymessage)

                apidata = {
                    'messageserialized': messageserialized.data,
                    'usersdataserialized': messagetonedata.data,
                    'allmessages': all_messages_folders_serializer.data
                }

                return Response(apidata, status=status.HTTP_200_OK)
            else:
                # dest12 = {"sender": f"{messagetone.reciever}", "reciever": f"{request.user}", "messageid": f"{id}",
                #           "messagetime": f"{vee}", "message": f"{keyword}", "image": False,
                #
                #           "senderid": f"{messagetone.reciever}",
                #           "receiverid": f"{request.user}",
                #           "id": message_id,
                #           "type": message_type,
                #           "from": sender_from,
                #           "quotedid": quoted_message_id,
                #           "message": message_content,
                #           "datetime": f"{vee}",
                #
                #           }
                jsondata = get_object_or_404(messagefolder, messageid=messagetone)
                # jsondata.testj.append(dest12)
                # jsondata.save()
                # mymessage = messagefolder.objects.filter(messageid=messagetone).first()
                # messageserialized = messageserializer(mymessage)

                data['datetime'] = str(vee)
                data['senderid'] = messagetone.reciever.id
                data['recieverid'] = request.user.id
                dest12 = data
                jsondata.testj.append(dest12)

                jsondata.save()
                mymessage = messagefolder.objects.filter(messageid=messagetone).first()
                messageserialized = messageserializer(mymessage)

                apidata = {
                    'messageserialized': messageserialized.data,
                    'usersdataserialized': messagetonedata.data,
                    'allmessages': all_messages_folders_serializer.data
                }

                return Response(apidata, status=status.HTTP_200_OK)

    mymessage = messagefolder.objects.filter(messageid=messagetone).first()
    messageserialized = messageserializer(mymessage)

    apidata = {
        'messageserialized': messageserialized.data,
        'usersdataserialized': messagetonedata.data,
        'allmessages': all_messages_folders_serializer.data
    }

    return Response(apidata, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def deletemessageportals(request, id):
    messagetone = get_object_or_404(messagestarter, messageid=id)
    messagetonedata = messagestarterserializer(messagetone)
    current_time = timezone.now()
    Profile.objects.update_or_create(
        user=request.user,
        defaults={'last_seen': current_time}
    )
    user = request.user
    # Query messages where the current user is either the sender or receiver
    messages = messagestarter.objects.filter(
        Q(sender=user) | Q(reciever=user)
    )

    # Query messagefolder model for all message IDs in the selected messages
    all_messages_folders = messagefolder.objects.filter(messageid__in=messages).all().order_by('-lastupdated')
    all_messages_folders_serializer = messageserializer(all_messages_folders, many=True)

    print(messagetone)
    vee = timezone.now()
    if request.method == 'POST':
        data = request.data.get('data_id')  # Assuming 'data' is the key containing the JSON payloa
        id_to_update = int(data)
        scans = messagefolder.objects.filter(messageid=messagetone).filter(
            testj__contains=[{"id": id_to_update}]).first()
        print('scan is', scans)

        # Retrieve the messagefolder object
        scan = messagefolder.objects.filter(messageid=messagetone).first()

        # Check if the object exists and if it has the specified ID in the `testj` field
        if scan and scan.testj:
            # Iterate through each JSON object in the `testj` field
            for item in scan.testj:
                # Check if the current object has the specified ID
                if int(item.get('id')) == id_to_update:
                    print('item is ', item)
                    # Update the fields of the JSON object
                    item['type'] = 'deleted'
                    # Save the changes to the database
                    scan.save()
                    break  # Exit the loop since the update is done

    mymessage = messagefolder.objects.filter(messageid=messagetone).first()
    messageserialized = messageserializer(mymessage)

    apidata = {
        'messageserialized': messageserialized.data,
        'usersdataserialized': messagetonedata.data,
        'allmessages': all_messages_folders_serializer.data
    }

    return Response(apidata, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def userjobs(request):
    current_time = timezone.now()
    Profile.objects.update_or_create(
        user=request.user,
        defaults={'last_seen': current_time}
    )
    user = request.user
    jobcard = Jobs.objects.all().order_by('-id')
    jobcardscount = Jobs.objects.all().count()
    jobserialized = Jobserializer(jobcard, many=True)

    context = {
        'jobcards': jobserialized.data,
        'jobcardscount': jobcardscount,
    }
    return Response(context, status=status.HTTP_200_OK)


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def userqrcards(request):
    qrcards = qrcodes.objects.all().order_by('-id')
    qrcardsserialized = QrcodeSerializer(qrcards, many=True)

    context = {
        'qrcards': qrcardsserialized.data,

    }
    return Response(context, status=status.HTTP_200_OK)






import random


def jobprint(request):
    # Generate a fake job title
    keywords = [
        "software development",
        "data science",
        "product management",
        "marketing management",
        "sales and business development",
        "customer support",
        "financial planning and analysis",
        "human resources",
        "user experience (UX) design",
        "user interface (UI) design",
        "full-stack development",
        "front-end development",
        "back-end development",
        "cloud computing",
        "DevOps",
        "database administration",
        "content marketing",
        "social media management",
        "content strategy",
        "cybersecurity",
        "network security",
        "IT support",
        "project coordination",
        "agile methodology",
        "quality control",
        "mobile app development",
        "web design and development",
        "e-commerce management",
        "SEO optimization",
        "data entry and analysis",
        "market research",
        "public relations",
        "event planning",
        "legal counsel",
        "health and safety management",
        "supply chain management",
        "logistics coordination",
        "environmental sustainability",
        "data visualization",
        "systems architecture",
        "brand management",
        "video production",
        "multimedia design",
        "gaming development",
        "education and training",
        "non-profit management",
        "project scheduling",
        "research and development",
        "healthcare administration",
        "hospitality management",
    ]

    job_description_templates = [
        "Join our team as a {job_title} in {job_location}. We are seeking a skilled {job_service} professional to {job_action}. Your role will involve {job_responsibilities}.",
        "Are you ready for a rewarding career as a {job_title} in {job_location}? We're looking for an experienced {job_service} expert to {job_action}. Your responsibilities will include {job_responsibilities}.",
        "We're hiring a {job_title} based in {job_location}. If you have expertise in {job_service}, apply now. You'll be responsible for {job_action} and {job_responsibilities}.",
        "As a {job_title} in {job_location}, you'll lead our {job_team} to {job_action}. Your role includes {job_responsibilities}.",
        "Become a {job_title} in {job_location} and make a difference in {job_service}. You'll be responsible for {job_action} and {job_responsibilities}.",
        "Join us as a {job_title} in {job_location}. We're looking for a {job_service} professional to {job_action}. Your contributions will include {job_responsibilities}.",
        "We're seeking a talented {job_title} based in {job_location}. If you're passionate about {job_service}, apply now. Your role involves {job_action} and {job_responsibilities}.",
        "As a {job_title} in {job_location}, you will work closely with our {job_team} to {job_action}. Your responsibilities include {job_responsibilities}.",
        "Start your career as a {job_title} in {job_location}. We need a {job_service} expert to {job_action}. Your role will encompass {job_responsibilities}.",
        "Join our {job_team} in {job_location} as a {job_title}. We're looking for someone with {job_service} skills to {job_action}. Your contributions will be in {job_responsibilities}.",
    ]

    # List of potential values for placeholders
    job_titles = ["Software Engineer", "Data Analyst", "Marketing Manager", "Sales Representative", "UX/UI Designer",
                  "Project Manager", "Financial Analyst", "Product Designer", "Customer Success Specialist",
                  "Business Analyst"]
    job_locations = ["New York", "San Francisco", "Los Angeles", "Chicago", "Boston", "London", "Berlin", "Tokyo",
                     "Sydney", "Toronto"]
    job_services = ["software development", "data analysis", "marketing strategy", "customer relations",
                    "financial analysis", "project management", "product design", "business development",
                    "quality assurance", "digital marketing"]
    job_actions = ["lead a team of professionals", "develop cutting-edge solutions", "drive marketing campaigns",
                   "manage client relationships", "analyze financial data", "oversee project delivery",
                   "design innovative products", "expand our market presence", "ensure product quality",
                   "optimize online advertising"]
    job_responsibilities = ["leading projects", "collaborating with cross-functional teams",
                            "delivering exceptional results", "meeting deadlines", "ensuring quality",
                            "driving innovation", "managing budgets", "implementing strategies",
                            "conducting data analysis", "customer acquisition"]
    job_teams = ["a talented group of professionals", "a cross-functional team", "our dedicated engineering team",
                 "a group of creative designers", "a high-performing sales team", "a dynamic marketing department",
                 "our innovative research team", "a customer-focused support team", "a skilled development team",
                 "a collaborative project management team"]

    # Generate a random job title
    user = User.objects.filter(id=10).first()
    for _ in range(10):
        job_title = fake.job()

        # Generate a random job location
        job_location = fake.city()

        job_description_template = random.choice(job_description_templates)
        job_title = job_title
        job_location = job_location
        job_service = random.choice(job_services)
        job_action = random.choice(job_actions)
        job_responsibility = random.choice(job_responsibilities)
        job_team = random.choice(job_teams)

        job_description = job_description_template.format(
            job_title=job_title,
            job_location=job_location,
            job_service=job_service,
            job_action=job_action,
            job_responsibilities=job_responsibility,
            job_team=job_team,
        )

        Jobs.objects.create(jobtitle=job_title, jobservice=random.choice(keywords), joblocation=job_location,
                            jobminimumexperience=10, jobdescription=job_description, user=user,
                            workinglevel='Senior Level', jobemploymenttype='Full-Time'
                            )

    return HttpResponse('hello world')


@permission_classes([IsAuthenticated])
@api_view(['GET'])
def userjobssinglepage(request, id):
    current_time = timezone.now()
    Profile.objects.update_or_create(
        user=request.user,
        defaults={'last_seen': current_time}
    )
    user = request.user
    jobcard = Jobs.objects.filter(id=id).first()
    jobserialized = Jobserializer(jobcard)

    context = {
        'jobcard': jobserialized.data,
    }
    return Response(context, status=status.HTTP_200_OK)


def timetest(request):
    vee = datetime.now().date().strftime("%Y-%m-%d %H:%M:%S")
    print(vee)
    current_datetime = timezone.now()
    veetwo = datetime.now()
    print(veetwo)

    return HttpResponse(f'{current_datetime}  hello  {veetwo} world')


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_job_application_page(request, id):
    user = User.objects.filter(id=10).first()
    user_profile = Profile.objects.filter(user=user).first()
    userprofile = Completeprofile(user_profile)
    try:
        jb = Jobs.objects.get(id=id)
    except Jobs.DoesNotExist:
        return JsonResponse({'saved': False, 'message': 'Job not found'})

    work_exp = workexperience.objects.filter(user=user).all()
    edu = University.objects.filter(user=user).all()

    if request.method == 'GET':
        my_jb = Jobserializer(jb)
        my_work_exp = Workexperienceserializer(work_exp, many=True)
        my_edu = Educationserializer(edu, many=True)

        context = {
            'job_detail': my_jb.data,
            'education_detail': my_edu.data,
            'work_experience': my_work_exp.data,
            'userprofile': userprofile.data

        }
        return Response(context, status=status.HTTP_200_OK)

    # Return an error response for unsupported methods
    return JsonResponse({'saved': False, 'message': 'Invalid request method'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def extract_hashtags(request, format=None):
    text = request.data.get('text', '')  # Get the text from the POST request data
    image = request.data.get('myimg')
    hashtags_with_symbol = re.findall(r'#\w+', text)  # Find words starting with #hashtags
    hashtags_without_symbol = [tag[1:] for tag in hashtags_with_symbol]  # Remove the # symbol

    s = shortuuid.ShortUUID(alphabet="0123456789")
    otp = s.random(length=15)

    # Create an instance of your model
    user = request.user
    your_model_instance = postings(message=text, messageid=otp, user=user, image=image if image else None)
    your_model_instance.save()

    # Add the hashtags as tags to the model instance
    your_model_instance.tags.add(*hashtags_without_symbol)

    serializer = postingserializer(your_model_instance)

    allposts = postings.objects.all().order_by('-id')
    postserializer = postingserializer(allposts, many=True)
    json_data_lists = []
    queryset2 = postings.tags.most_common()[:4]
    common_tags = queryset2.annotate(num_times=Count('taggit_taggeditem_items'))
    for a in common_tags:
        # Construct a dictionary with the desired data
        datas = {"name": a.slug, "number": a.num_times}  # Replace with your data

        # Append the dictionary to the list
        json_data_lists.append(datas)

    context = {
        'allposts': postserializer.data,
        'trending': json_data_lists,
    }
    return Response(context, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def Timeline(request):
    current_time = timezone.now()
    Profile.objects.update_or_create(
        user=request.user,
        defaults={'last_seen': current_time}
    )
    user = request.user
    allposts = postings.objects.all().order_by('-id')
    postserializer = postingserializer(allposts, many=True)
    queryset2 = postings.tags.most_common()[:4]
    myprofile = Profile.objects.filter(user=request.user).first()
    myprofileserializer = ProfileSerializer(myprofile)
    # Exclude the current user by ID
    all_records_except_current_user = Profile.objects.all().exclude(user=request.user).order_by('?')[:2]

    profileserializer = ProfileSerializer(all_records_except_current_user, many=True)
    json_data_lists = []
    common_tags = queryset2.annotate(num_times=Count('taggit_taggeditem_items'))
    for a in common_tags:
        # Construct a dictionary with the desired data
        datas = {"name": a.slug, "number": a.num_times}  # Replace with your data

        # Append the dictionary to the list
        json_data_lists.append(datas)

    context = {
        'allposts': postserializer.data,
        'trending': json_data_lists,
        'profileserializer': profileserializer.data,
        'myprofileserializer': myprofileserializer.data
    }
    return Response(context, status=status.HTTP_200_OK)


from django.core import serializers


class CommonTagAPIView(APIView):
    def get(self, request):
        # Query the common tags
        # allposts = postings.objects.all().order_by('-id')
        # postserializer = tagspostingserializer(allposts, many=True)
        myuser = User.objects.filter(id=11).first()

        # Exclude the current user by ID
        all_records_except_current_user = Profile.objects.all().exclude(user=myuser).order_by('?')[:2]

        # Serialize the shuffled queryset using the Userserializer
        profileserializer = ProfileSerializer(all_records_except_current_user, many=True)
        queryset2 = postings.tags.most_common()[:4]
        json_data_lists = []
        common_tags = queryset2.annotate(num_times=Count('taggit_taggeditem_items'))
        for a in common_tags:
            # Construct a dictionary with the desired data
            datas = {"name": a.slug, "number": a.num_times}  # Replace with your data

            # Append the dictionary to the list
            json_data_lists.append(datas)

        context = {
            # 'allposts': postserializer.data,
            'tagdata': json_data_lists,
            'all_records_except_current_user': profileserializer.data
        }
        return Response(context, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def savedtimelinepost(request):
    queryset2 = postings.tags.most_common()[:4]
    json_data_lists = []
    common_tags = queryset2.annotate(num_times=Count('taggit_taggeditem_items'))
    for a in common_tags:
        # Construct a dictionary with the desired data
        datas = {"name": a.slug, "number": a.num_times}  # Replace with your data

        # Append the dictionary to the list
        json_data_lists.append(datas)
    myuser = request.user
    if request.method == 'POST':
        # Get the post ID from the POST data
        post_id = request.data.get('post_id')

        # Retrieve the post object from the database
        try:
            post = postings.objects.get(messageid=post_id)
        except postings.DoesNotExist:
            return JsonResponse({'saved': False, 'message': 'Post not found'})

        # Check if the post is already saved by the current user
        if post.likes.filter(id=myuser.id).exists():
            # If yes, remove the current user from the post's saved_by ManyToMany field
            post.likes.remove(myuser)
            saved = False
            message = 'Post unliked'
            post = postings.objects.filter(messageid=post_id).first()
            postserialized = postingserializer(post)
            slug = request.data.get('tagslug')
            if (slug):
                tag = get_object_or_404(Tag, slug=slug)
                post = postings.objects.filter(tags=tag).order_by('-id')
                postserialized = postingserializer(post, many=True)

                context = {
                    'allposts': postserialized.data,
                    'saved': saved,
                    'message': message,
                    'tagdata': json_data_lists,
                }

                return Response(context, status=status.HTTP_200_OK)
            else:

                allposts = postings.objects.all().order_by('-id')
                postserializer = postingserializer(allposts, many=True)
                context = {
                    'allposts': postserializer.data,
                    'saved': saved,
                    'message': message,
                    'tagdata': json_data_lists,
                }

                return Response(context, status=status.HTTP_200_OK)
        else:
            # If no, add the current user to the post's saved_by ManyToMany field
            post.likes.add(myuser)
            saved = True
            message = 'Post liked'
            user = myuser
            post = postings.objects.filter(messageid=post_id).first()
            postserialized = postingserializer(post)

            slug = request.data.get('tagslug')
            if (slug):
                tag = get_object_or_404(Tag, slug=slug)
                posts = postings.objects.filter(tags=tag).order_by('-id')
                postserialized = postingserializer(posts, many=True)
                context = {
                    'allposts': postserialized.data,
                    'saved': saved,
                    'message': message,
                    'tagdata': json_data_lists,
                }

                return Response(context, status=status.HTTP_200_OK)

            else:

                allposts = postings.objects.all().order_by('-id')
                postserializer = postingserializer(allposts, many=True)

                context = {
                    'allposts': postserializer.data,
                    'saved': saved,
                    'message': message,
                    'tagdata': json_data_lists,

                }

                return Response(context, status=status.HTTP_200_OK)

    # Return an error response for unsupported methods
    return JsonResponse({'saved': False, 'message': 'Invalid request method'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def newcomment(request, id):
    json_data_lists = []
    queryset2 = postings.tags.most_common()[:4]
    common_tags = queryset2.annotate(num_times=Count('taggit_taggeditem_items'))
    s = shortuuid.ShortUUID(alphabet="0123456789")
    otp = s.random(length=15)

    for a in common_tags:
        # Construct a dictionary with the desired data
        datas = {"name": a.slug, "number": a.num_times}  # Replace with your data

        # Append the dictionary to the list
        json_data_lists.append(datas)

    quizdata = []
    ves = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    a = get_object_or_404(postings, messageid=id)

    if request.method == 'POST':
        myimage = request.data.get('myimg')
        keyword = request.data.get('keyword')
        post_id = request.data.get('tagslug')
        print(keyword)
        if myimage:
            serializer = UploadedImage.objects.create(image=myimage)
            serializer.save()
            serializeddata = Imagetest(serializer)
            dest12 = {"sender": f"{request.user.username}", "senderid": f"{request.user.id}", "commentid": f"{otp}",
                      "messagetime": f"{ves}", "message": f"{keyword}"}

            a.testj.append(dest12)
            a.save()
            if (post_id):
                tag = get_object_or_404(Tag, slug=post_id)
                post = postings.objects.filter(tags=tag).order_by('-id')
                postserialized = postingserializer(post, many=True)
                apidata = {
                    'message': 'Comment Added Successfully',
                    'allposts': postingserializer.data,
                    'trending': json_data_lists,
                    'mypost': postingserializer.data,
                }
                return Response(apidata, status=status.HTTP_200_OK)
            else:

                allposts = postings.objects.all().order_by('-id')
                postserializer = postingserializer(allposts, many=True)
            apidata = {
                'message': 'Comment Added Successfully',
                'allposts': postserializer.data,
                'trending': json_data_lists,
                # 'mypost': postserialized.data,
            }
            return Response(apidata, status=status.HTTP_200_OK)

        else:
            dest12 = {"sender": f"{request.user.username}", "senderid": f"{request.user.id}", "commentid": f"{id}",
                      "messagetime": f"{ves}", "message": f"{keyword}"}
            # jsondata = get_object_or_404(postings, messageid=id)
            a.testj.append(dest12)
            a.save()
            if (post_id):
                tag = get_object_or_404(Tag, slug=post_id)
                post = postings.objects.filter(tags=tag).order_by('-id')
                postserialized = postingserializer(post, many=True)

                apidata = {
                    'message': 'Comment Added Successfully',
                    'allposts': postserialized.data,
                    'trending': json_data_lists,
                    'mypost': postserialized.data,
                }

                return Response(apidata, status=status.HTTP_200_OK)
            else:

                allposts = postings.objects.all().order_by('-id')
                postserializer = postingserializer(allposts, many=True)
                apidata = {
                    'message': 'Comment Added Successfully',
                    'allposts': postserializer.data,
                    'trending': json_data_lists,
                    'mypost': postserializer.data,
                }

                return Response(apidata, status=status.HTTP_200_OK)

    return Response({'message': 'We Are Unable To Process Your Request'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def postingsinglepage(request, id):
    current_time = timezone.now()
    Profile.objects.update_or_create(
        user=request.user,
        defaults={'last_seen': current_time}
    )
    user = request.user
    post = postings.objects.filter(messageid=id).first()
    if post:
        postserialized = postingserializer(post)

        context = {
            'mypost': postserialized.data,
        }
        return Response(context, status=status.HTTP_200_OK)
    else:
        return Response({'message': 'We Are Unable To Process Your Request'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def applications(request, pk):
    s = shortuuid.ShortUUID(alphabet="0123456789")
    otp = s.random(length=16)
    jb = get_object_or_404(Jobs, id=pk)
    if Applications.objects.filter(user=request.user).filter(jobapplied=jb).exists():
        context = {

            'message': 'You Have Already Applied For This Role'
        }

        return Response(context, status=status.HTTP_200_OK)
    else:
        Applications.objects.create(user=request.user, author=jb.user, application_id=otp,
                                    jobapplied=jb)
        context = {

            'message': 'Application Submitted'
        }

        return Response(context, status=status.HTTP_200_OK)


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def tagged(request, slug):
    user = request.user
    tag = get_object_or_404(Tag, slug=slug)
    post = postings.objects.filter(tags=tag).order_by('-id')
    postserialized = postingserializer(post, many=True)
    queryset2 = postings.tags.most_common()[:4]
    myprofile = Profile.objects.filter(user=user).first()
    myprofileserializer = ProfileSerializer(myprofile)
    # Exclude the current user by ID
    all_records_except_current_user = Profile.objects.all().exclude(user=user).order_by('?')[:2]

    profileserializer = ProfileSerializer(all_records_except_current_user, many=True)
    json_data_lists = []
    common_tags = queryset2.annotate(num_times=Count('taggit_taggeditem_items'))
    for a in common_tags:
        # Construct a dictionary with the desired data
        datas = {"name": a.slug, "number": a.num_times}  # Replace with your data

        # Append the dictionary to the list
        json_data_lists.append(datas)

    context = {
        'message': 'Successfully Fetched',
        'allposts': postserialized.data,
        'trending': json_data_lists,
        'profileserializer': profileserializer.data,
        'myprofileserializer': myprofileserializer.data
    }
    return Response(context, status=status.HTTP_200_OK)


class SearchEmployeeByPhoneNumberAPIView(APIView):
    def get(self, request):
        phone_number = request.query_params.get('phone_number', None)

        if phone_number is None:
            return Response({"error": "Phone number parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            employee = employees.objects.get(phone_number=phone_number)
            serializer = EmployeesSerializer(employee)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except employees.DoesNotExist:
            return Response({"error": "No employee found with the provided phone number."},
                            status=status.HTTP_404_NOT_FOUND)




@api_view(['POST'])
def upload_image(request):
    if request.method == 'POST':
        image_data = request.FILES.get('myaudio')
        serializerz = Image.objects.create(image=image_data)
        serializerz.save()
        serializer = ImageSerializer(serializerz)
        return Response(serializer.data, status=status.HTTP_201_CREATED)





@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def create_company(request):
    data = request.data
    company_name = data.get('companyName')
    logo = request.FILES.get('logo')

    if not company_name or not logo:
        return Response({'error': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)

    # Check if the user already exists
    try:
        user = User.objects.get(username=company_name)
        # Check if the user already has an associated company
        if hasattr(user, 'company'):
            return Response({'error': 'Company already exists for this user'}, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        # Create a new user
        user = User.objects.create_user(
            username=company_name,
            email=f'admin@{company_name}.com',
            password='test'
        )

    # Create a new company instance
    company_instance = company(
        user=user,
        organization_name=company_name,
        logo=logo  # Directly set the uploaded logo file
    )

    company_instance.save()

    return Response({'message': 'Company created successfully'}, status=status.HTTP_201_CREATED)




class UniversityListCreateView(generics.ListCreateAPIView):
    queryset = exceltest.objects.all()
    serializer_class = Universitydata

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)



@api_view(['GET'])
def seodetail(request, id):

    jobdetails = get_object_or_404(Jobs, id=id)
    jobdetail = seoserializer(jobdetails)
    context = {
        'jobdetail': jobdetail.data,
    }

    return Response(context, status=status.HTTP_200_OK)

@api_view(['GET'])
def alljobcards(request):
    jobcard = Jobs.objects.all().order_by('-id')
    jobserialized = Jobserializer(jobcard, many=True)
    context = {
        'jobdetail': jobserialized.data,
    }

    return Response(context, status=status.HTTP_200_OK)