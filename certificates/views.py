import mimetypes

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
        # Obtém o estudante associado ao usuário logado
        try:
            student = Student.objects.get(user=request.user)
        except Student.DoesNotExist:
            return Response(
                {"error": "Student not found for the logged-in user."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Adiciona o student_id ao request.data
        data = request.data.copy()
        data["student"] = student.id

        # Valida e salva o certificado
        serializer = CertificateSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CertificatePreviewView(APIView):

    def get(self, request, pk, *args, **kwargs):
        certificate = get_object_or_404(Certificate, pk=pk)
        file = open(certificate.file.path, "rb")

        content_type, _ = mimetypes.guess_type(certificate.file.name)
        response = FileResponse(file, content_type=content_type)

        response["Content-Disposition"] = f'inline; filename="{certificate.file.name}"'
        return response


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
