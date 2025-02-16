from django.contrib.auth.models import User
from rest_framework import serializers
from django.db import transaction
from rest_framework.serializers import (
    CharField,
    DateTimeField,
    EmailField,
    Field,
    IntegerField,
    ModelSerializer,
    PrimaryKeyRelatedField,
    SerializerMethodField,
)

from courses.models import Course
from courses.serializers import CourseSerializer

from .models import Student


class StudentSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    email = serializers.EmailField(source="user.email", read_only=True)
    course_name = serializers.CharField(source="course.name", read_only=True)  
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all(), write_only=True)  

    class Meta:
        model = Student
        fields = ["id", "full_name", "email", "course", "course_name"]

    def get_full_name(self, obj):
        return obj.full_name

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", None)  
        course_data = validated_data.pop("course", None)  

        if user_data and "email" in user_data:
            instance.user.email = user_data["email"]
            instance.user.save()

        if course_data:
            instance.course = course_data

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance



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
