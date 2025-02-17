from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from drf_spectacular.utils import extend_schema
from enrollments.models import Enrollment
from django.shortcuts import get_object_or_404
from professors.models import Professor

from .models import Date, Event
from .serializers import (
    CreateEventSerializer,
    DateSerializer,
    EventEnrollmentSerializer,
    EventSerializer,
)

class EventUpdateView(APIView):
    def put(self, request, id, *args, **kwargs):
        try:
            event = Event.objects.get(id=id)
        except Event.DoesNotExist:
            return Response({"error": "Evento não encontrado."}, status=status.HTTP_404_NOT_FOUND)

        serializer = EventSerializer(event, data=request.data, partial=True) 
        if serializer.is_valid():
            updated_event = serializer.save()
            return Response(EventSerializer(updated_event).data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DateCreateView(APIView):
    serializer_class = DateSerializer

    def post(self, request, *args, **kwargs):

        serializer = DateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class DateUpdateView(APIView):
    def put(self, request, id, *args, **kwargs):
        try:
            date = Date.objects.get(id=id)
        except Date.DoesNotExist:
            return Response({"error": "Data não encontrada."}, status=status.HTTP_404_NOT_FOUND)

        serializer = DateSerializer(date, data=request.data, partial=True) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DateListView(APIView):
    def get(self, request, *args, **kwargs):
        dates = Date.objects.all()
        serializer = DateSerializer(dates, many=True)
        return Response(serializer.data)


class EventListView(APIView):
    @extend_schema(
        responses={200: EventSerializer(many=True)}  
    )
    def get(self, request, *args, **kwargs):
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)


class EventCreateView(APIView):
    serializer_class = CreateEventSerializer

    def post(self, request, *args, **kwargs):

        data = request.data.copy()
        data["creator"] = request.user.id

        serializer = CreateEventSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EventDetailView(APIView):
    def get(self, request, pk, *args, **kwargs):
        try:
            event = Event.objects.get(pk=pk)
            serializer = EventSerializer(event)
            return Response(serializer.data)
        except Event.DoesNotExist:
            return Response(
                {"error": "Evento não encontrado."}, status=status.HTTP_404_NOT_FOUND
            )
        
class EventDeleteView(APIView):
    def delete(self, request, id, *args, **kwargs):
        event = get_object_or_404(Event, id=id)

        if request.user != event.creator:
            return Response({"error": "Você não tem permissão para deletar este evento."}, status=status.HTTP_403_FORBIDDEN)

        event.delete()
        return Response({"message": "Evento deletado com sucesso!"}, status=status.HTTP_204_NO_CONTENT)
        
class StudentEnrolledEventsView(ListAPIView):
    serializer_class = EventEnrollmentSerializer

    def get_queryset(self):
        student_id = self.kwargs.get("student_id")

        enrollments = Enrollment.objects.filter(student_id=student_id)
        event_ids = enrollments.values_list("event_id", flat=True)
        return Event.objects.filter(id__in=event_ids)

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class ProfessorCreatedEventsView(ListAPIView):
    serializer_class = EventSerializer

    def get_queryset(self):
        professor_id = self.kwargs.get("professor_id")
        professor = get_object_or_404(Professor, id=professor_id)

        return Event.objects.filter(creator=professor.user)

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)

            return Response(serializer.data, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=400)
        

