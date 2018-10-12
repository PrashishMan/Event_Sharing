from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token

from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response

from django.utils.six import BytesIO
from rest_framework.parsers import JSONParser

from django.contrib.auth.models import User

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

from django.http import HttpResponse
from django.contrib.auth import authenticate

from rest_framework.decorators import authentication_classes, permission_classes
# Create your views here.
def testApi(request):
    return HttpResponse("Hello")

@api_view
def login_user(response):
    pass


@receiver(post_save, sender= settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance = None, created = False, **kwargs):
    if created:
        Token.objects.create(user = instance)

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data = request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user = user)
        return Response({
            'token' : token.key,
            'user_id': user.pk,
            'email': user.email
        })

@api_view(['POST'])
def login_user(request):
    stream = BytesIO(request.body)
    data = dict(JSONParser().parse(stream))

    token = getToken(data)
    if token is None:
        return Response({"Result" : "UnSuccess", "Error" : "Invalid Credentials"})

    return Response({"Result" : "Success","Token" : str(token)})

def getToken(data):
    username = data.get('username')
    password = data.get('password')

    user = authenticate(username = username, password = password)

    if user is not None:
        user_token = Token.objects.get(user = user)
        return user_token

    return None


