from io import BytesIO

import qrcode
from django.core.files import File
from django.db import transaction, IntegrityError
from django.http import HttpResponse
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiExample, OpenApiParameter, extend_schema
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Enrollment
from students.models import Student
from .models import Enrollment, Event
from .serializers import CreateEnrollmentSerializer, EnrollmentSerializer


class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer

    def get_serializer_class(self):
        if self.action == "create":
            return CreateEnrollmentSerializer
        return EnrollmentSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        user_id = request.user.id  
        try:
            student = Student.objects.get(user_id=user_id)  
            student_id = student.id 
            print(f"✅ Student encontrado no banco: {student_id} (User: {user_id})")  
        except Student.DoesNotExist:
            print(f"❌ Erro: Nenhum estudante encontrado para User ID {user_id}")
            return Response({"error": "Estudante não encontrado."}, status=status.HTTP_400_BAD_REQUEST) 

        event_id = request.data.get("event")

        try:
            student = Student.objects.get(user_id=user_id)  
            print(f"✅ Student encontrado no banco: {student.id} (User: {user_id})")  
        except Student.DoesNotExist:
            print(f"❌ Erro: Nenhum estudante encontrado para User ID {user_id}")
            return Response({"error": "Estudante não encontrado."}, status=status.HTTP_400_BAD_REQUEST)

        event = Event.objects.select_for_update().get(id=event_id)

        if Enrollment.objects.filter(student_id=student_id, event_id=event_id).exists():
            return Response({"error": "Você já está inscrito neste evento!"}, status=status.HTTP_400_BAD_REQUEST)

        if event.slots <= 0:
            return Response(
                {"error": "Não há vagas disponíveis para este evento."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        data = request.data.copy()
        data["student"] = request.user.id

        enrollment_data = {"student": student.id, "event": event_id}
        print("📤 Dados enviados ao serializer:", enrollment_data)

        serializer = self.get_serializer(data=enrollment_data)
        if not serializer.is_valid():
            print(f"❌ Erro de validação: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.is_valid(raise_exception=True)
        enrollment = serializer.save()
        print(f"✅ Inscrição criada com sucesso: {enrollment}")
        
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(f"enrollment:{enrollment.id}")
        qr.make(fit=True)

        img = qr.make_image(fill="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)

        enrollment.qr_code.save(f"qr_{enrollment.id}.png", File(buffer), save=True)

        event.slots -= 1
        event.save()

        response = HttpResponse(buffer.getvalue(), content_type="image/png")
        response["Content-Disposition"] = f"attachment; filename=qr_{enrollment.id}.png"
        return response

    @transaction.atomic
    def destroy(self, request, *args, **kwargs):

        enrollment = self.get_object()
        event = enrollment.event

        event.slots += 1
        event.save()

        enrollment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AttendanceValidationView(APIView):

    @extend_schema(
        request={
            "application/json": {
                "type": "object",
                "properties": {
                    "enrollment_id": {
                        "type": "integer",
                        "description": "ID da inscrição",
                    },
                },
                "required": ["enrollment_id"],
            }
        },
        responses={
            200: EnrollmentSerializer,
            404: EnrollmentSerializer,
        },
    )
    def post(self, request, *args, **kwargs):
        enrollment_id = request.data.get("enrollment_id")
        try:
            enrollment = Enrollment.objects.get(id=enrollment_id)
            enrollment.attended = True
            enrollment.save()
            return Response(
                {"message": "Presença validada com sucesso."}, status=status.HTTP_200_OK
            )
        except Enrollment.DoesNotExist:
            return Response(
                {"error": "Inscrição não encontrada."}, status=status.HTTP_404_NOT_FOUND
            )
