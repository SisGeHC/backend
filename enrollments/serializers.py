from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from events.serializers import EventSerializer
from students.serializers import StudentSerializer
from students.models import Student
from .models import Enrollment


class EnrollmentSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())  # ✅ Pegando Student corretamente
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
