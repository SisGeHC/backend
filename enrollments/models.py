from django.conf import settings
from django.db.models import CASCADE, BooleanField, ForeignKey, ImageField, Model

from events.models import Event


class Enrollment(Model):
    student = ForeignKey(
        "students.Student", on_delete=CASCADE, related_name="enrollments"
    )
    event = ForeignKey(Event, on_delete=CASCADE, related_name="enrollments")
    qr_code = ImageField(upload_to="qr_codes/", blank=True, null=True)
    attended = BooleanField(default=False)

    class Meta:
        unique_together = ("student", "event")

    def __str__(self):
        return f"{self.student.user.username} - {self.event.title}"
