from django.contrib.auth.models import User
from django.db import transaction
from rest_framework.serializers import (
    CharField,
    DateTimeField,
    EmailField,
    Field,
    ModelSerializer,
    SerializerMethodField,
)

from .models import Coordinator


class CoordinatorSerializer(ModelSerializer):
    full_name = SerializerMethodField()
    email = EmailField(source="user.email", read_only=True)
    created_at = DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updated_at = DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = Coordinator
        fields = ["id", "full_name", "email", "created_at", "updated_at"]

    def get_full_name(self, obj):

        return obj.full_name


class CoordinatorCreateSerializer(ModelSerializer):

    username = CharField(write_only=True)
    password = CharField(write_only=True)
    email = EmailField(write_only=True)
    first_name = CharField(write_only=True)
    last_name = CharField(write_only=True)

    class Meta:
        model = Coordinator
        fields = [
            "username",
            "password",
            "email",
            "first_name",
            "last_name",
        ]

    def create(self, validated_data):

        user_data = {
            "username": validated_data.pop("username"),
            "password": validated_data.pop("password"),
            "email": validated_data.pop("email"),
            "first_name": validated_data.pop("first_name"),
            "last_name": validated_data.pop("last_name"),
        }

        with transaction.atomic():

            user = User.objects.create_user(**user_data)
            user.set_password(user_data["password"])
            user.save()

            coordinator = Coordinator.objects.create(
                user=user,
            )

        return coordinator
