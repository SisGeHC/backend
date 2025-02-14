from django.db import models
from users.models import User, Teacher, Student
from django.utils import timezone


def get_default_user():
    return User.objects.filter(role="teacher").first()


class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_closed = models.BooleanField(default=False)

    # Apenas professores podem criar eventos
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        default=get_default_user,
        null=False,  # Agora é obrigatório
        blank=False,
        # Apenas professores podem ser escolhidos
        limit_choices_to={'role': 'teacher'},
    )

    def __str__(self):
        return self.title


class Enrollment(models.Model):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="enrollments")
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name="enrollments")
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Garante que um aluno não possa se inscrever mais de uma vez
        unique_together = ('student', 'event')

    def __str__(self):
        return f"{self.student.username} -> {self.event.title}"


class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    attended_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Evita registros duplicados de presença
        unique_together = ('student', 'event')

    def __str__(self):
        return f"{self.student.username} - {self.event.title} (Presente)"
