from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.serializers import (
    CharField,
    EmailField,
    Serializer,
    ValidationError,
)


class CustomAuthTokenSerializer(Serializer):
    email = EmailField()
    password = CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise ValidationError("User not found")

        user = authenticate(username=user.username, password=password)
        if not user:
            raise ValidationError("Invalid")

        attrs["user"] = user
        return attrs


from django.contrib.auth import authenticate
from rest_framework import serializers


class ChangePasswordSerializer(Serializer):
    old_password = CharField(required=True)
    new_password = CharField(required=True)

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not authenticate(username=user.username, password=value):
            raise ValidationError("Senha atual incorreta.")
        return value
