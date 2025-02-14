from django.shortcuts import render
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema, OpenApiParameter, extend_schema_view
from rest_framework import viewsets
from .models import Certificate
from .serializers import CertificateSerializer
from rest_framework.generics import GenericAPIView
from certificates.serializers import ValidateCertificateSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from certificates.models import Certificate
from certificates.serializers import CertificateSerializer
from users.permissions import IsCoordinator

@extend_schema_view(
    list=extend_schema(
        summary="Listar Certificados",
        description="Lista os certificados. Estudantes veem apenas os próprios. Coordenadores veem apenas os pendentes.",
        parameters=[
            OpenApiParameter(name="status", description="Filtrar por status (pending, approved, rejected)", required=False, type=str),
        ],
        tags=["Certificados"]
    ),
    retrieve=extend_schema(
        summary="Obter Detalhes de um Certificado",
        description="Recupera os detalhes de um certificado específico.",
        tags=["Certificados"]
    ),
    create=extend_schema(
        summary="Criar um Certificado",
        description="Permite que **apenas estudantes** criem certificados. O status sempre começa como `pending`.",
        request=CertificateSerializer,
        responses={201: CertificateSerializer},
        tags=["Certificados"]
    ),
    update=extend_schema(
        summary="Atualizar um Certificado",
        description="**Apenas o estudante dono do certificado pode editar**.",
        request=CertificateSerializer,
        responses={200: CertificateSerializer},
        tags=["Certificados"]
    ),
    destroy=extend_schema(
        summary="Deletar um Certificado",
        description="**Apenas o estudante dono do certificado pode deletar**.",
        tags=["Certificados"]
    ),
)
class CertificateViewSet(viewsets.ModelViewSet):
    queryset = Certificate.objects.all()
    serializer_class = CertificateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'student':
            return Certificate.objects.filter(student=user)
        elif user.role == 'coordinator':
            return Certificate.objects.filter(status="pending")
        return Certificate.objects.none()

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.student != request.user:
            return Response({"error": "Você não tem permissão para editar este certificado."}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.student != request.user:
            return Response({"error": "Você não tem permissão para deletar este certificado."}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)

    @extend_schema(
        summary="Validar Certificado",
        description="Permite que **coordenadores** aprovem ou rejeitem certificados pendentes.",
        request=ValidateCertificateSerializer,
        responses={200: {"message": "Certificado validado com sucesso!"}},
        tags=["Certificados"]
    )
    @action(detail=True, methods=['patch'], permission_classes=[IsAuthenticated, IsCoordinator])
    def validate(self, request, pk=None):
        certificate = self.get_object()
        if certificate.status != "pending":
            return Response({"error": "Este certificado já foi validado."}, status=status.HTTP_400_BAD_REQUEST)

        status_choice = request.data.get("status", "").lower()
        if status_choice not in ["approved", "rejected"]:
            return Response({"error": "Escolha um status válido ('approved' ou 'rejected')."}, status=status.HTTP_400_BAD_REQUEST)

        certificate.status = status_choice
        certificate.validated_by = request.user
        certificate.save()

        if status_choice == "approved":
            certificate.student.hours_completed += certificate.hours
            certificate.student.save()

        return Response({"message": f"Certificado {status_choice} com sucesso!"}, status=status.HTTP_200_OK)





