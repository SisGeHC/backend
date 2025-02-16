from django.conf import settings
from django.db.models import (
    CASCADE,
    CharField,
    DateField,
    ForeignKey,
    ManyToManyField,
    Model,
    PositiveIntegerField,
    TextField,
    TimeField,
)


class Date(Model):
    day = DateField()
    start_time = TimeField()
    end_time = TimeField()

    def __str__(self):
        return f"{self.day} - {self.start_time} to {self.end_time}"


class Event(Model):
    title = CharField(max_length=200)
    description = TextField()
    location = CharField(max_length=200)
    category = CharField(max_length=200)
    dates = ManyToManyField(Date, related_name="events")
    creator = ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=CASCADE, related_name="created_events"
    )
    slots = PositiveIntegerField(default=0)

    def __str__(self):
        return self.title
