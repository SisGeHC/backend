from rest_framework import serializers
from rest_framework.serializers import CharField, ModelSerializer, Serializer

from events.serializers import EventSerializer
from students.models import Student
from students.serializers import StudentSerializer

from .models import Enrollment


class EnrollmentSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())
    event = EventSerializer(read_only=True)

    class Meta:
        model = Enrollment
        fields = ["id", "student", "event", "qr_code", "attended"]
        read_only_fields = ["qr_code", "attended"]


class CreateEnrollmentSerializer(ModelSerializer):

    class Meta:
        model = Enrollment
        fields = ["id", "student", "event", "qr_code", "attended"]
        read_only_fields = ["qr_code", "attended"]


class EmailSerializer(Serializer):

    message = CharField()

    class Meta:

        fields = ["message"]
