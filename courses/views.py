from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.decorators import action
from courses.models import Course
from courses.serializers import CourseSerializer
from users.permissions import IsCoordinator
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Course
from .serializers import CourseSerializer
from users.permissions import IsCoordinator

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            self.permission_classes = [AllowAny]  # Qualquer usuário pode listar ou visualizar cursos
        elif self.action in ["update", "partial_update"]:
            self.permission_classes = [IsAuthenticated, IsCoordinator]  # Apenas Coordenadores podem atualizar cursos
        elif self.action in ["create"]:  
            self.permission_classes = [IsAdminUser]  # Apenas Superusuários podem criar cursos
        return super().get_permissions()
    
    @extend_schema(
        summary="Inscrever-se em um curso",
        description="Permite que alunos se inscrevam em um curso pelo ID.",
        tags=["Cursos"],
        responses={201: {"message": "Inscrição realizada com sucesso!"}},
    )
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def enroll(self, request, pk=None):
        user = request.user
        course = self.get_object()

        # Verifica se o usuário é um estudante
        if user.role != "student":
            return Response({"error": "Apenas alunos podem se inscrever em cursos."}, status=status.HTTP_403_FORBIDDEN)

        # Verifica se o aluno já está inscrito
        if course.students.filter(id=user.id).exists():
            return Response({"error": "Você já está inscrito neste curso."}, status=status.HTTP_400_BAD_REQUEST)

        # Inscreve o aluno no curso
        course.students.add(user)

        return Response({"message": "Inscrição realizada com sucesso!"}, status=status.HTTP_201_CREATED)
    @extend_schema(
        summary="Cancelar inscrição em um curso",
        description="Permite que alunos saiam de um curso pelo ID.",
        tags=["Cursos"],
        responses={200: {"message": "Você saiu do curso com sucesso!"}},
    )
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def unenroll(self, request, pk=None):
        user = request.user  # Corrigido
        course = self.get_object()

        if user.role != "student":  # Corrigido
            return Response({"error": "Apenas alunos podem sair de cursos."}, status=status.HTTP_403_FORBIDDEN)

        if user not in course.students.all():
            return Response({"error": "Você não está inscrito neste curso."}, status=status.HTTP_400_BAD_REQUEST)

        course.students.remove(user)
        return Response({"message": "Você saiu do curso com sucesso!"}, status=status.HTTP_200_OK)



