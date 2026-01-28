from rest_framework import serializers
from users.models import User

class RegistrationSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    patronymic = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    password_repeat = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        if data['password'] != data['password_repeat']:
            raise serializers.ValidationError({"password": "Пароли не совпадают"})
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({"email": "Email уже используется"})
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            patronymic=validated_data.get('patronymic', '')
        )
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'patronymic', 'email', 'created_at', 'is_active'] # doesn't show password for security
        read_only_fields = ['id', 'created_at', 'is_active']
