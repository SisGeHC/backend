from rest_framework import serializers
from rest_framework.serializers import CharField, ModelSerializer, Serializer

from events.serializers import EventSerializer
from students.models import Student
from students.serializers import StudentSerializer

from .models import Enrollment
from django.conf import settings

class EnrollmentSerializer(serializers.ModelSerializer):

    student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())  
    event = EventSerializer(read_only=True)  
    qr_code_url = serializers.SerializerMethodField()  


    class Meta:
        model = Enrollment
        fields = ["id", "student", "event", "qr_code", "qr_code_url", "attended"] 
        read_only_fields = ["qr_code", "qr_code_url", "attended"]

    def get_qr_code_url(self, obj):
        if obj.qr_code:
            return f"{settings.MEDIA_URL}{obj.qr_code}"  
        return None


class CreateEnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = ["id", "student", "event", "qr_code", "attended"]
        read_only_fields = ["qr_code", "attended"]


class EmailSerializer(Serializer):

    message = CharField()

    class Meta:

        fields = ["message"]
