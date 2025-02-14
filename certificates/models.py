from django.db import models
from users.models import Student
from django.core.exceptions import ValidationError
from django.utils import timezone

def validate_certificate_file(value):
    valid_extensions = [".pdf", ".jpg", ".jpeg", ".png"]
    if not any(value.name.lower().endswith(ext) for ext in valid_extensions):
        raise ValidationError("Apenas arquivos PDF, JPG, JPEG e PNG são permitidos.")

class Certificate(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pendente'),
        ('approved', 'Aprovado'),
        ('rejected', 'Rejeitado'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="certificates")
    file = models.FileField(upload_to="certificates/", validators=[validate_certificate_file])
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    hours = models.PositiveIntegerField()
    comment = models.TextField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    validated_at = models.DateTimeField(blank=True, null=True)

    def approve(self, coordinator):
        self.status = "approved"
        self.validated_at = timezone.now()
        self.student.hours_completed += self.hours
        self.student.save()
        self.save()

    def reject(self, coordinator, comment=""):
        self.status = "rejected"
        self.validated_at = timezone.now()
        self.comment = comment
        self.save()

    def __str__(self):
        return f"Certificado de {self.student.username} - {self.status}"
