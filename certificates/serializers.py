import os

from rest_framework.serializers import (
    DateTimeField,
    ModelSerializer,
    PrimaryKeyRelatedField,
    ValidationError,
)

from students.models import Student
from students.serializers import StudentSerializer

from .models import Certificate


class CertificateSerializer(ModelSerializer):
    student = PrimaryKeyRelatedField(queryset=Student.objects.all())
    created_at = DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updated_at = DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = Certificate
        fields = [
            "id",
            "student",
            "file",
            "status",
            "hours_taken",
            "created_at",
            "updated_at",
        ]

    def validate_file(self, value):
        allowed_extensions = [".png", ".jpeg"]
        ext = os.path.splitext(value.name)[1]  # Pega a extensão do arquivo
        if ext.lower() not in allowed_extensions:
            raise ValidationError(
                f"Tipo de arquivo não suportado. Use: {', '.join(allowed_extensions)}"
            )
        return value

    def to_representation(self, instance):

        representation = super().to_representation(instance)
        representation["student"] = StudentSerializer(instance.student).data
        return representation
