from django.db.models import CharField, IntegerField, Model


class Course(Model):

    name = CharField(max_length=255)
    complementary_hours_needed = IntegerField(default=0)

    def __str__(self):
        return self.name
