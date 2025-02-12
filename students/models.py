from django.contrib.auth.models import User
from django.db.models import CASCADE, ForeignKey, IntegerField, Model, OneToOneField

from courses.models import Course


class Student(Model):
    user = OneToOneField(User, on_delete=CASCADE)
    course = ForeignKey(Course, on_delete=CASCADE, related_name="students")
    complementary_hours = IntegerField(default=0)
