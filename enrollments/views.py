from io import BytesIO

import qrcode
import requests
from django.core.files import File
from django.db import transaction
from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from students.models import Student
from students.services import send_student_email

from .models import Enrollment, Event
from .serializers import (
    CreateEnrollmentSerializer,
    EmailSerializer,
    EnrollmentSerializer,
)


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
        except Student.DoesNotExist:
            return Response(
                {"error": "Estudante não encontrado."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        event_id = request.data.get("event")

        try:
            event = Event.objects.select_for_update().get(id=event_id)
        except Event.DoesNotExist:
            return Response(
                {"error": "Evento não encontrado."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if Enrollment.objects.filter(student_id=student.id, event_id=event_id).exists():
            return Response(
                {"error": "Você já está inscrito neste evento!"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if event.slots <= 0:
            return Response(
                {"error": "Não há vagas disponíveis para este evento."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        enrollment_data = {"student": student.id, "event": event_id}
        serializer = self.get_serializer(data=enrollment_data)
        serializer.is_valid(raise_exception=True)
        enrollment = serializer.save()

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

        url = "https://api.imgbb.com/1/upload"
        params = {"key": "95d39d279af969953fb408be8d0ea421"}
        files = {"image": buffer.getvalue()}

        response = requests.post(url, params=params, files=files)
        if response.status_code == 200:
            image_url = response.json()["data"]["url"]

        send_student_email(
            self,
            student=student,
            subject="Confirmação de Inscrição no Evento",
            template_name="emails/email_confirmation.html",
            context={
                "student_name": student.user.get_full_name(),
                "event_title": event.title,
                "event_date": event.dates.first().day.strftime("%d/%m/%Y"),
                "event_time": event.dates.first().start_time.strftime("%H:%M"),
                "event_location": event.location,
                "event_category": event.category,
                "qr_code_url": image_url,
            },
        )

        response = HttpResponse(buffer.getvalue(), content_type="image/png")
        response["Content-Disposition"] = f"inline; filename=qr_{enrollment.id}.png"
        return response
    
    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        enrollment = self.get_object()
        event = enrollment.event

        event.slots += 1
        event.save()

        enrollment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def send_enrollment_email(self, student, event, qr_code_url):
        subject = "Confirmação de Inscrição no Evento"
        context = {
            "student_name": student.user.get_full_name(),
            "event_title": event.title,
            "event_date": event.dates.first().day.strftime("%d/%m/%Y"),
            "event_time": event.dates.first().start_time.strftime("%H:%M"),
            "event_location": event.location,
            "event_category": event.category,
            "qr_code_url": qr_code_url,  
        }

        html_message = render_to_string("emails/email_confirmation.html", context)
        plain_message = strip_tags(html_message)

        send_mail(
            subject,
            plain_message,
            settings.DEFAULT_FROM_EMAIL,
            [student.user.email],
            html_message=html_message,
        )

class AttendanceValidationView(APIView):
    def get(self, request, enrollment_id, *args, **kwargs):  
        if not enrollment_id:
            return Response({"error": "ID da matrícula não fornecido."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            enrollment = Enrollment.objects.get(id=enrollment_id)
            
            if enrollment.attended:
                return Response(
                    {
                        "status": "already_confirmed",
                        "message": "Presença já confirmada!",
                        "attended": True,
                    },
                    status=status.HTTP_200_OK,
                )

            enrollment.attended = True
            enrollment.save()

            return Response(
                {
                    "status": "success",
                    "message": "Presença confirmada com sucesso!",
                    "attended": True,
                    "student": enrollment.student.user.get_full_name(),
                    "event": enrollment.event.title,
                    "date": enrollment.event.dates.first().day.strftime("%d/%m/%Y"),
                    "location": enrollment.event.location,
                },
                status=status.HTTP_200_OK,
            )

        except Enrollment.DoesNotExist:
            return Response(
                {"error": "Inscrição não encontrada."},
                status=status.HTTP_404_NOT_FOUND,
            )



            

class SendEventNotificationView(APIView):
    serializer_class = EmailSerializer

    @transaction.atomic
    def post(self, request, event_id, *args, **kwargs):

        serializer = EmailSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        message = serializer.validated_data["message"]

        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            return Response(
                {"error": "Evento não encontrado."},
                status=status.HTTP_404_NOT_FOUND,
            )

        enrollments = Enrollment.objects.filter(event=event)
        if not enrollments.exists():
            return Response(
                {"error": "Nenhum aluno inscrito neste evento."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        for enrollment in enrollments:
            send_student_email(
                self,
                student=enrollment.student,
                subject=f"Notificação do Evento: {event.title}",
                template_name="emails/event_notification_email.html",
                context={
                    "student_name": enrollment.student.user.get_full_name(),
                    "event_title": event.title,
                    "event_date": event.dates.first().day.strftime("%d/%m/%Y"),
                    "event_time": event.dates.first().start_time.strftime("%H:%M"),
                    "event_location": event.location,
                    "message": message,
                },
            )

        return Response(
            {"message": f"Notificação enviada para {enrollments.count()} alunos."},
            status=status.HTTP_200_OK,
        )
