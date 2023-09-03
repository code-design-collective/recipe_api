from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .serializers import UserSerializer

@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    user = User.objects.filter(email=email).first()

    if user is None or not user.check_password(password):
        return Response({"detail": "Invalid credentials."}, status=status.HTTP_400_BAD_REQUEST)

    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(instance=user)

    return Response({"token": token.key, "user": serializer.data})


@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        email = serializer.validated_data.get('email')
        password = request.data.get('password')

        user, created = User.objects.get_or_create(email=email)
        user.set_password(password)
        user.save()

        token, created = Token.objects.get_or_create(user=user)

        return Response({"token": token.key, "user": serializer.data})

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    return Response(f"Passed for {request.user.email}")
