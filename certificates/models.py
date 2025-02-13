from django.db import models
from users.models import User
from events.models import Event

class Certificate(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    file = models.FileField(upload_to='certificates/')
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ], default='pending')

    def __str__(self):
        return f"Certificate of {self.student.username} for {self.event.title}"
