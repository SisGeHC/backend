from django.db import models
from django.conf import settings

from django.db import models
from django.conf import settings

class Course(models.Model):
    name = models.CharField(max_length=255, unique=True)

    students = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="student_courses", 
        blank=True
    )

    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="teacher_courses"
    )

    coordinator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="coordinator_courses"
    )

    def __str__(self):
        return self.name

