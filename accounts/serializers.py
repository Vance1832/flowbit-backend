from rest_framework import serializers
from .models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = (
            "id",
            "name",
            "phone_country_code",
            "phone_number",
            "phone",
            "email",
            "password",
            "confirm_password",
        )
        read_only_fields = ("id", "phone")

    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError("Passwords do not match.")

        return attrs

    def create(self, validated_data):
        validated_data.pop("confirm_password")

        password = validated_data.pop("password")

        user = User(**validated_data)
        user.set_password(password)
        user.role = User.Role.USER
        user.status = User.Status.ACTIVE
        user.save()

        return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "name",
            "phone_country_code",
            "phone_number",
            "phone",
            "email",
            "role",
            "status",
            "phone_verified",
            "email_verified",
        )
        read_only_fields = fields


from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = "phone"

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token["name"] = user.name
        token["phone"] = user.phone
        token["role"] = user.role

        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        data["user"] = {
            "id": self.user.id,
            "name": self.user.name,
            "phone": self.user.phone,
            "role": self.user.role,
            "status": self.user.status,
        }

        return data