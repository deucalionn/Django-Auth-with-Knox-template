from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import ValidationError
from django.contrib.auth import authenticate
from knox.models import AuthToken


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        if not username or not password or not email:
            raise ValidationError(
                "Username, email, and password are required.")

        if User.objects.filter(username=username).exists():
            raise ValidationError("Username is already taken.")

        User.objects.create_user(
            username=username, email=email, password=password)

        return Response({'message': 'User registered successfully',
                         'token': AuthToken.objects.create(User.objects.get(
                             username=username))[1]},
                        status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        # get user object associate to the username and password
        user = authenticate(username=username, password=password)
        if not user:
            return Response({'error': 'Invalid credentials'},
                            status=status.HTTP_401_UNAUTHORIZED)

        token = AuthToken.objects.create(user)[1]  # create token for the user
        return Response({
            'token': token,
            'username': user.username
        }, status=status.HTTP_200_OK)
