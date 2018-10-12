from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework import authentication, permissions
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from authentication import views as auth_view

from django.http import HttpResponse


from .models import Profile



from django.utils.six import BytesIO

import json
from django.contrib.auth.models import User

from .serializers import UserSerializer, CreateUserSerializer, ProfileSerialzier



# Create your views here.
def homeView(request):
    return HttpResponse("hello")

@api_view(['GET'])
def testApi(request):
    if (request.method == 'GET'):
        return Response({"key" : "value"}, status = status.HTTP_200_OK)

@api_view(['POST'])
def registerUser(request):
    stream = BytesIO(request.body)
    data = JSONParser().parse(stream)

    serializer = CreateUserSerializer(data=data)
    print("Is serializer valid")
    print(serializer.is_valid())
    print(data)

    if serializer.is_valid():
        print("saving user ...")
        serializer.create_save(serializer.validated_data)

        print("user saved")
        return Response({"success": True}, status=status.HTTP_201_CREATED)

    else:
        print("Error: ")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserView(APIView):
    authentication_classes = (authentication.TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )
    def get(self, request, user_id = ''):
        if user_id:
            profile = Profile.objects.get(id = user_id)
            serializer = ProfileSerialzier(profile)

        else:
            profiles = Profile.objects.all()
            profile_list = []
            for profile in profiles:
                profile_dict = dict(ProfileSerialzier(profile).data)

                user = profile.user
                user_dict = dict(UserSerializer(user).data)

                for index, key in enumerate(user_dict):
                    profile_dict[key] = user_dict[key]

                profile_list.append(profile_dict)

        return Response({"profiles" : profile_list}, status= status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        pass
        # stream = BytesIO(request.body)
        # data = JSONParser().parse(stream)
        #
        # serializer = CreateUserSerializer(data=data)
        # print("Is serializer valid")
        # print(serializer.is_valid())
        # print(data)
        #
        # if serializer.is_valid():
        #     print("saving user ...")
        #     serializer.create_save(serializer.validated_data)
        #
        #     print("user saved")
        #     return  Response({"success" : "True"}, status=status.HTTP_201_CREATED)
        #
        # else:
        #     print("Error: ")
        #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def create_fb_user(request):
    stream = BytesIO(request.body)
    user_data = JSONParser().parse(stream)

    data = {}
    data['firstname'] = user_data.get('name').split(' ')[0]
    data['lastname'] = user_data.get('name').split(' ')[-1]
    data['email'] = user_data.get('email')
    data['username'] = user_data.get('id')
    data['password'] = user_data.get('id')[4:10] + str(user_data.get('email').split('@')[0]) + user_data.get('id')[2:-8:3]
    user = createUser(data)
    print(" Printng token")
    token = Token.objects.get_or_create(user=user)
    print(token)
    return Response({"token" : str(token), "success": True})

def createUser(data):
    user = User.objects.create(username=data.get('username'), email=data.get('email'),
                               first_name=data.get('firstname'), last_name=data.get('lastname'))
    user.set_password(data.get('password'))
    user.save()
    return user

@api_view(['POST'])
def checkUserExists(request):
    stream  = BytesIO(request.body)
    user_data = JSONParser().parse(stream)
    data = {}
    data['username'] = user_data.get('id')
    data['password'] = user_data.get('id')[4:10] + str(user_data.get('email').split('@')[0]) + user_data.get('id')[
                                                                                               2:-8:3]
    token = auth_view.getToken(data)
    print(token)

    return Response({"isAvailable": (str(token) != None), "token" : str(token)})








