import mimetypes
from django.conf import settings
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from students.models import Student

from .models import Certificate
from .serializers import CertificateSerializer


class CertificatePreviewView(APIView):
    def get(self, request, id):
        certificate = get_object_or_404(Certificate, id=id)

        if not certificate.file:
            return Response({"error": "Certificado não encontrado."}, status=404)

        file_url = f"{settings.MEDIA_URL}{certificate.file}"
        full_url = request.build_absolute_uri(file_url)  # URL completa para o frontend

        return Response({"file_url": full_url}, status=200)

class CertificateListView(ListAPIView):

    queryset = Certificate.objects.all()
    serializer_class = CertificateSerializer


class CertificateCreateView(APIView):

    parser_classes = [MultiPartParser, FormParser]

    @extend_schema(
        request={
            "multipart/form-data": {
                "type": "object",
                "properties": {
                    "student": {"type": "integer"},
                    "file": {
                        "type": "string",
                        "format": "binary",
                    },
                },
            },
        },
        responses={201: CertificateSerializer},
        description="Upload a certificate file for a student.",
    )
    def post(self, request, *args, **kwargs):
        serializer = CertificateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CertificateCreateView(APIView):

    parser_classes = [MultiPartParser, FormParser]

    @extend_schema(
        request={
            "multipart/form-data": {
                "type": "object",
                "properties": {
                    "file": {
                        "type": "string",
                        "format": "binary",
                    },
                    "hours_taken": {
                        "type": "integer",
                    },
                },
            },
        },
        responses={201: CertificateSerializer},
        description="Upload a certificate file for the logged-in student.",
    )
    def post(self, request, *args, **kwargs):

        try:
            student = Student.objects.get(user=request.user)
        except Student.DoesNotExist:
            return Response(
                {"error": "Student not found for the logged-in user."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        data = request.data.copy()
        data["student"] = student.id

        serializer = CertificateSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CertificateUpdateView(APIView):

    @extend_schema(
        request=CertificateSerializer,
        responses={200: CertificateSerializer},
    )
    def patch(self, request, pk, *args, **kwargs):

        certificate = get_object_or_404(Certificate, pk=pk)

        serializer = CertificateSerializer(certificate, data=request.data, partial=True)
        if serializer.is_valid():

            serializer.save()

            student = certificate.student
            student.complementary_hours += certificate.hours_taken
            student.save()

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
