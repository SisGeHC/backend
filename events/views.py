from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from events.models import Event
from events.serializers import EventSerializer
from users.permissions import IsStudent, IsTeacherOrCoordinator
from django.utils import timezone

@extend_schema_view(
    list=extend_schema(summary="Listar todos os eventos", tags=["Eventos"]),
    retrieve=extend_schema(summary="Detalhes de um evento", tags=["Eventos"]),
    create=extend_schema(summary="Criar um evento", tags=["Eventos"]),
    partial_update=extend_schema(
        summary="Editar um evento",
        description="Permite que professores editem apenas seus próprios eventos e coordenadores editem qualquer evento.",
        parameters=[
            OpenApiParameter(name="id", description="ID do evento a ser atualizado", required=True, type=int)
        ],
        tags=["Eventos"]
    ),
    destroy=extend_schema(summary="Deletar um evento", tags=["Eventos"]),
)
class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get_permissions(self):
        if self.action in ["create", "destroy", "update", "partial_update"]:
            self.permission_classes = [IsAuthenticated, IsTeacherOrCoordinator]
        return super().get_permissions()
    
    def destroy(self, request, *args, **kwargs):
        event = self.get_object()

        # Verifica se o usuário tem permissão para deletar o evento
        if request.user.role == "coordinator" or event.created_by == request.user:
            event.delete()
            return Response({"message": "Evento deletado com sucesso!"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "Você não tem permissão para excluir este evento."}, status=status.HTTP_403_FORBIDDEN)


    @extend_schema(
        summary="Listar eventos disponíveis para inscrição",
        description="Retorna todos os eventos que ainda aceitam inscrições.",
        tags=["Eventos"],
    )
    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def available(self, request):
        events = Event.objects.filter(is_closed=False, start_time__gte=timezone.now())
        serializer = self.get_serializer(events, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Inscrever-se em um evento",
        description="Permite que um estudante se inscreva em um evento pelo ID.",
        tags=["Eventos"],
        responses={201: {"message": "Inscrição realizada com sucesso!"}},
    )
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsStudent])
    def register(self, request, pk=None):
        event = self.get_object()
        student = request.user

        # Verifica se já está inscrito
        if event.students.filter(id=student.id).exists():
            return Response({"error": "Você já está inscrito neste evento."}, status=status.HTTP_400_BAD_REQUEST)

        event.students.add(student)
        return Response({"message": "Inscrição realizada com sucesso!"}, status=status.HTTP_201_CREATED)
    
    @extend_schema(
        summary="Atualizar um evento (parcial ou completo)",
        description=(
            "Permite que **professores** editem **apenas seus próprios eventos** e **coordenadores** editem **qualquer evento**. "    
        ),
        tags=["Eventos"],
        request=EventSerializer,
        responses={
            200: EventSerializer,
            403: {"description": "Você não tem permissão para editar este evento."},
        }
    )
    def update(self, request, *args, **kwargs):
        event = self.get_object()

        # Coordenadores podem editar qualquer evento
        if request.user.role == "coordinator":
            return super().update(request, *args, **kwargs)

        # Professores só podem editar eventos que criaram
        if request.user.role == "teacher" and event.created_by == request.user:
            return super().update(request, *args, **kwargs)

        return Response(
            {"error": "Você não tem permissão para editar este evento."},
            status=status.HTTP_403_FORBIDDEN,
        )
    
    @extend_schema(
        summary="Obter os detalhes de um evento para edição",
        description="Retorna todos os detalhes de um evento específico pelo ID para que possa ser editado.",
        tags=["Eventos"],
        responses={200: EventSerializer}
    )
    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def get_event_data(self, request, pk=None):
        event = self.get_object()
        serializer = self.get_serializer(event)
        return Response(serializer.data)




