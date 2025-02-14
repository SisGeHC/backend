from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.decorators import action
from courses.models import Course
from courses.serializers import CourseSerializer
from users.permissions import IsCoordinator

@extend_schema_view(
    list=extend_schema(summary="Listar todos os cursos", tags=["Cursos"]),
    retrieve=extend_schema(summary="Detalhes de um curso", tags=["Cursos"]),
    create=extend_schema(summary="Criar um curso", tags=["Cursos"]),
    update=extend_schema(summary="Atualizar um curso", tags=["Cursos"]),
    partial_update=extend_schema(summary="Atualização parcial de um curso", tags=["Cursos"]),
    destroy=extend_schema(summary="Deletar um curso", tags=["Cursos"]),
)

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            self.permission_classes = [AllowAny]  # Qualquer usuário pode listar ou visualizar cursos
        elif self.action in ["update", "partial_update"]:
            self.permission_classes = [IsAuthenticated, IsCoordinator]  # Apenas Coordenador podem atualizar cursos
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

        if student.role != "student":
            return Response({"error": "Apenas alunos podem se inscrever em cursos."}, status=status.HTTP_403_FORBIDDEN)

        if student.student_course:
            return Response({"error": "Você já está inscrito em um curso. Saia primeiro para se inscrever em outro."}, status=status.HTTP_400_BAD_REQUEST)

        course.students.add(student)
        return Response({"message": "Inscrição realizada com sucesso!"}, status=status.HTTP_201_CREATED)

    @extend_schema(
        summary="Cancelar inscrição em um curso",
        description="Permite que alunos saiam de um curso pelo ID.",
        tags=["Cursos"],
        responses={200: {"message": "Você saiu do curso com sucesso!"}},
    )
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def unenroll(self, request, pk=None):
        user = request.user
        course = self.get_object()

        if student.role != "student":
            return Response({"error": "Apenas alunos podem sair de cursos."}, status=status.HTTP_403_FORBIDDEN)

        if student not in course.students.all():
            return Response({"error": "Você não está inscrito neste curso."}, status=status.HTTP_400_BAD_REQUEST)

        course.students.remove(student)
        return Response({"message": "Você saiu do curso com sucesso!"}, status=status.HTTP_200_OK)

