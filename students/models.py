from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models import (
    CASCADE,
    DateTimeField,
    ForeignKey,
    Model,
    OneToOneField,
    PositiveIntegerField,
)
from django.utils import timezone

from courses.models import Course


class Student(Model):
    user = OneToOneField(User, on_delete=CASCADE)
    course = ForeignKey(Course, on_delete=CASCADE, related_name="students")
    complementary_hours = PositiveIntegerField(default=0)
    created_at = DateTimeField(default=timezone.now)
    updated_at = DateTimeField(auto_now=True, null=True)

    @property
    def full_name(self):
        return f"{self.user.first_name} {self.user.last_name}"

    def email_student(
        self,
        subject,
        message,
        html_message,
        from_email=None,
        **kwargs,
    ):
        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            html_message=html_message,
            recipient_list=[self.user.email],
            **kwargs,
        )

    def __str__(self):

        return f"{self.user.first_name} {self.user.last_name}"
