from rest_framework import serializers
from rest_framework.serializers import (
    DateField,
    ModelSerializer,
    PrimaryKeyRelatedField,
    TimeField,
)
from datetime import timedelta
from coordinators.models import Coordinator
from coordinators.serializers import CoordinatorSerializer, SerializerMethodField
from professors.models import Professor
from professors.serializers import ProfessorSerializer

from .models import Date, Event


class DateSerializer(ModelSerializer):
    day = DateField(format="%d/%m/%Y")
    start_time = TimeField(format="%H:%M")
    end_time = TimeField(format="%H:%M")

    class Meta:
        model = Date
        fields = ["id", "day", "start_time", "end_time"]


class CreateEventSerializer(ModelSerializer):
    dates = PrimaryKeyRelatedField(queryset=Date.objects.all(), many=True)

    class Meta:
        model = Event
        fields = [
            "id",
            "title",
            "description",
            "location",
            "category",
            "creator",
            "dates",
            "slots",
        ]


class EventSerializer(ModelSerializer):
    dates = DateSerializer(many=True, read_only=True)
    creator = SerializerMethodField()

    class Meta:
        model = Event
        fields = [
            "id",
            "title",
            "description",
            "location",
            "category",
            "dates",
            "creator",
            "slots", 
            'start_time', 
            'end_time'
        ]

    def get_creator(self, obj):

        if Professor.objects.filter(user=obj.creator).exists():
            professor = Professor.objects.get(user=obj.creator)
            return ProfessorSerializer(professor).data

        elif Coordinator.objects.filter(user=obj.creator).exists():
            coordinator = Coordinator.objects.get(user=obj.creator)
            return CoordinatorSerializer(coordinator).data

        return obj.creator.id
    

class EventEnrollmentSerializer(EventSerializer):

    class Meta(EventSerializer.Meta):
        fields = EventSerializer.Meta.fields