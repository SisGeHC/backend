from django.db import models
from users.models import User
from events.models import Event

class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    attendance_confirmed = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.student.username} - {self.event.title}"
