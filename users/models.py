from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework_simplejwt.tokens import OutstandingToken

class User(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('coordinator', 'Coordinator'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    email = models.EmailField(unique=True)  # Garante que o email seja único
    USERNAME_FIELD = 'email'  # Define o email como campo de login
    REQUIRED_FIELDS = ['username']  # O username é obrigatório

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="custom_user_groups",
        blank=True
    )

    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="custom_user_permissions",
        blank=True
    )



class Student(User):
    hours_completed = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.username} (Student)"
    
class Teacher(User):
    pass  # Pode adicionar mais tarde caso precise

class Coordinator(Teacher):
    pass  # Pode adicionar mais tarde caso precise



