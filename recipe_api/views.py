from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from .serializers import UserSerializer


def index(request):
    return render(request, 'home.html')


@api_view(['POST'])
def login(request):
    print('LOGIN! 🔑')
    user = get_object_or_404(User, username=request.data['username'])
    # Todo determine if not found or wrong pw, add status code
    if not user.check_password(request.data['password']):
        return Response({"detail": "Not found."})

    token, created = Token.objects.get_or_create(user=user)
    serialzer = UserSerializer(instance=user)

    return Response({"token": token.key, "user": serialzer.data})


@api_view(['POST'])
def signup(request):
    print('SIGNUP! 📝')
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=request.data['username'])
        user.set_password(request.data['password'])
        user.save()
        token = Token.objects.create(user=user)

        return Response({"token": token.key, "user": serializer.data})

    return Response(serializer.errors)


@api_view(['POST'])
def test_token(request):
    print('TEST TOKEN! 🪙')
    return Response({})
