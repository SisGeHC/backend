from django.db.models import (
    CASCADE,
    CharField,
    DateTimeField,
    FileField,
    ForeignKey,
    Model,
    PositiveIntegerField,
)
from django.utils import timezone

from students.models import Student


class Certificate(Model):

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("denied", "Denied"),
        ("approved", "Approved"),
    ]

    student = ForeignKey(Student, on_delete=CASCADE, related_name="certificates")
    file = FileField(upload_to="certificates/")
    status = CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    hours_taken = PositiveIntegerField(default=0)
    created_at = DateTimeField(default=timezone.now)
    updated_at = DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"Certificate of {self.student.user.get_full_name()} - {self.status}"
