from rest_framework.serializers import ModelSerializer

from events.serializers import EventSerializer
from students.serializers import StudentSerializer

from .models import Enrollment


class EnrollmentSerializer(ModelSerializer):
    student = StudentSerializer()
    event = EventSerializer()

    class Meta:
        model = Enrollment
        fields = ["id", "student", "event", "qr_code", "attended"]
        read_only_fields = ["qr_code", "attended"]


class CreateEnrollmentSerializer(ModelSerializer):

    class Meta:
        model = Enrollment
        fields = ["id", "student", "event", "qr_code", "attended"]
        read_only_fields = ["qr_code", "attended"]
