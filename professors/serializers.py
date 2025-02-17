from django.contrib.auth.models import User
from django.db import transaction
from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response
from rest_framework.serializers import (
    CharField,
    DateTimeField,
    EmailField,
    ModelSerializer,
    PrimaryKeyRelatedField,
    SerializerMethodField,
    ValidationError,
)

from courses.models import Course
from courses.serializers import CourseSerializer

from .models import Professor


class ProfessorSerializer(ModelSerializer):
    full_name = SerializerMethodField()
    email = EmailField(source="user.email")
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
    created_at = DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updated_at = DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    course_name = serializers.CharField(source="course.name", read_only=True)  

    class Meta:
        model = Professor
        fields = ["id", "full_name", "email", "course", "course_name", "created_at", "updated_at"]

    def get_full_name(self, obj):

        return obj.full_name
    
    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", None)  
        course_data = validated_data.pop("course", None)  

        if user_data and "email" in user_data:
            instance.user.email = user_data["email"]
            instance.user.save()

        if course_data:  
            try:
                course_instance = Course.objects.get(name=course_data["name"])  
                instance.course = course_instance  
            except Course.DoesNotExist:
                raise serializers.ValidationError({"course": "Curso não encontrado."})

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class ProfessorCreateSerializer(ModelSerializer):

    username = CharField(write_only=True)
    password = CharField(write_only=True)
    email = EmailField(write_only=True)
    first_name = CharField(write_only=True)
    last_name = CharField(write_only=True)

    course = PrimaryKeyRelatedField(queryset=Course.objects.all(), write_only=True)

    class Meta:
        model = Professor
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
            if User.objects.filter(email=user_data["email"]).exists():
                raise ValidationError({"email": "Este email já está em uso."})

            user = User.objects.create_user(**user_data)
            user.set_password(user_data["password"])
            user.save()

            professor = Professor.objects.create(
                user=user,
                course=validated_data["course"],
            )

        return professor
