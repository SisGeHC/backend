from django.contrib.auth.models import User
from django.db.models import CASCADE, DateTimeField, ForeignKey, Model, OneToOneField
from django.utils import timezone

from courses.models import Course


class Professor(Model):
    user = OneToOneField(User, on_delete=CASCADE)
    course = ForeignKey(Course, on_delete=CASCADE, related_name="professors")
    created_at = DateTimeField(default=timezone.now)
    updated_at = DateTimeField(auto_now=True, null=True)

    @property
    def full_name(self):
        return f"{self.user.first_name} {self.user.last_name}"


def __str__(self):

    return f"{self.user.first_name} {self.user.last_name}"
