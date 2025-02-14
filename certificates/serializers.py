from rest_framework import serializers
from .models import Certificate


class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = '__all__'


class ValidateCertificateSerializer(serializers.Serializer):
    certificate_id = serializers.IntegerField()
    status = serializers.CharField()
    message = serializers.CharField()


class CertificateSerializer(serializers.ModelSerializer):
    file = serializers.FileField()

    class Meta:
        model = Certificate
        fields = "__all__"
        read_only_fields = ["status", "validated_at", "submitted_at"]

    def create(self, validated_data):
        validated_data["status"] = "pending"
        return super().create(validated_data)
