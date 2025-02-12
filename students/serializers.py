from django.contrib.auth.models import User
from django.db import transaction
from rest_framework.serializers import (
    CharField,
    EmailField,
    IntegerField,
    ModelSerializer,
    PrimaryKeyRelatedField,
    SerializerMethodField,
)

from courses.models import Course
from courses.serializers import CourseSerializer

from .models import Student


class StudentSerializer(ModelSerializer):
    full_name = SerializerMethodField()
    email = EmailField(source="user.email")
    course = CourseSerializer()
    complementary_hours = IntegerField(read_only=True)

    class Meta:
        model = Student
        fields = ["id", "full_name", "email", "course", "complementary_hours"]

    def get_full_name(self, obj):

        return f"{obj.user.first_name} {obj.user.last_name}"


class StudentCreateSerializer(ModelSerializer):

    username = CharField(write_only=True)
    password = CharField(write_only=True)
    email = EmailField(write_only=True)
    first_name = CharField(write_only=True)
    last_name = CharField(write_only=True)

    course = PrimaryKeyRelatedField(queryset=Course.objects.all(), write_only=True)

    class Meta:
        model = Student
        fields = [
            "username",
            "password",
            "email",
            "first_name",
            "last_name",
            "course",
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

            student = Student.objects.create(
                user=user,
                course=validated_data["course"],
            )

        return student
