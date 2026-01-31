import jwt
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .authentication import JWTAuthentication
from .serializers import RegistrationSerializer, UserProfileSerializer
from users.models import User
from datetime import timedelta, datetime, timezone
from django.conf import settings

class RegistrationView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.create(serializer.validated_data)
            return Response({"message": "Пользователь зарегистрирован"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({"error": "Email и пароль обязательны"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(email=email).first()
        if not user or not user.check_password(password) or not user.is_active:
            return Response({"error": "Неверные учетные данные или аккаунт неактивен"}, status=status.HTTP_401_UNAUTHORIZED)

        payload = {'user_id': user.id, 'exp': datetime.now(timezone.utc) + timedelta(days=1)}  # so that jwt token expires in 1 day
        token = jwt.encode(payload, settings.JWT_SECRET, algorithm='HS256')

        return Response({"token": token}, status=status.HTTP_200_OK)


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)


class LogoutView(APIView):
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        return Response({"Успешный выход из аккаунта"}, status=status.HTTP_200_OK)
