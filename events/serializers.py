from rest_framework import serializers
from events.models import Event
from users.serializers import UserSerializer

class EventSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Event
        fields = ["id", "title", "description", "category", "created_at", "start_time", "end_time", "is_closed", "created_by"]
