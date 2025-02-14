from django.contrib.auth.models import User
from django.db.models import CASCADE, DateTimeField, Model, OneToOneField
from django.utils import timezone


class Coordinator(Model):
    user = OneToOneField(User, on_delete=CASCADE)
    created_at = DateTimeField(default=timezone.now)
    updated_at = DateTimeField(auto_now=True, null=True)

    @property
    def full_name(self):
        return f"{self.user.first_name} {self.user.last_name}"


def __str__(self):

    return f"{self.user.first_name} {self.user.last_name}"
