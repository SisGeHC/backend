from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status, permissions
from drf_spectacular.utils import extend_schema, OpenApiExample
from django.contrib.auth import authenticate
from .serializers import UserSerializer, TeacherSerializer
from django.contrib.auth.hashers import make_password
from .serializers import CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from users.permissions import IsStudent, IsTeacher, IsCoordinator
from rest_framework.generics import DestroyAPIView, GenericAPIView
from users.serializers import DashboardSerializer

from rest_framework import permissions
from django.shortcuts import get_object_or_404
from .models import User, Student
from .serializers import UserSerializer, StudentSerializer
from rest_framework import serializers
import logging
logger = logging.getLogger(__name__)

# Serializer para documentação no Swagger
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

class LoginView(APIView):
    @extend_schema(
        request=LoginSerializer,
        responses={
            200: {
                "type": "object",
                "properties": {
                    "refresh": {"type": "string", "example": "exemplo_refresh_token"},
                    "access": {"type": "string", "example": "exemplo_access_token"},
                    "user": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "integer", "example": 1},
                            "username": {"type": "string", "example": "fabio"},
                            "email": {"type": "string", "example": "fabio@email.com"},
                            "role": {"type": "string", "example": "student"}
                        }
                    }
                }
            },
            400: {
                "type": "object",
                "properties": {
                    "error": {"type": "string", "example": "Email e senha são obrigatórios."}
                }
            },
            401: {
                "type": "object",
                "properties": {
                    "error": {"type": "string", "example": "Credenciais inválidas."}
                }
            },
        },
        examples=[
            OpenApiExample(
                "Exemplo de requisição",
                value={"email": "usuario@example.com", "password": "senha123"},
                request_only=True
            ),
            OpenApiExample(
                "Exemplo de resposta",
                value={
                    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                    "user": {
                        "id": 1,
                        "username": "usuario",
                        "email": "usuario@example.com",
                        "role": "student"
                    }
                },
                response_only=True
            ),
        ],
        description="Autentica o usuário e retorna um token JWT",
        summary="Login",
        tags=["Autenticação"],
    )
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        logger.info(f"Tentativa de login com email: {email}")

        if not email or not password:
            return Response(
                {"error": "Email e senha são obrigatórios."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(email=email)
            logger.info(f"Usuário encontrado: {user.username}")
        except User.DoesNotExist:
            logger.error("Usuário não encontrado")
            return Response(
                {"error": "Credenciais inválidas."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        user = authenticate(username=email, password=password)
        if not user:
            logger.error("Autenticação falhou")
            return Response(
                {"error": "Credenciais inválidas."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        logger.info("Autenticação bem-sucedida")
        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role
            }
        }, status=status.HTTP_200_OK)

class UpdateUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        request=UserSerializer,
        responses={200: UserSerializer},
        description="Atualiza parcialmente as informações do usuário",
        summary="Atualizar usuário",
        tags=["Usuários"],
    )
    def patch(self, request, id):
        user_to_update = get_object_or_404(User, id=id)

        # O usuário só pode editar a si mesmo, exceto se for coordenador
        if request.user != user_to_update and request.user.role != "coordinator":
            return Response({"error": "Você não tem permissão para editar este usuário."}, status=status.HTTP_403_FORBIDDEN)

        data = request.data.copy()

        if "role" in data and request.user.role != "coordinator":
            return Response({"error": "Você não pode alterar seu próprio papel (role)."}, status=status.HTTP_403_FORBIDDEN)

        if user_to_update.role == "student" and request.user.role == "student":
            allowed_fields = ["first_name", "last_name", "email", "username", "horasComplementares"]
            data = {key: value for key, value in data.items() if key in allowed_fields}

        if request.user.role == "teacher" and "horasComplementares" in data:
            return Response({"error": "Professores não podem modificar as horas complementares dos alunos."}, status=status.HTTP_403_FORBIDDEN)

        if request.user.role == "coordinator":
            serializer = UserSerializer(user_to_update, data=data, partial=True)
        else:
            serializer = UserSerializer(user_to_update, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]  # Apenas usuários autenticados podem acessar

    @extend_schema(
        responses={200: UserSerializer},
        description="Obtém os detalhes do usuário autenticado.",
        summary="Obter usuário atual",
        tags=["Usuários"],
    )
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

class DeleteUserView(DestroyAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer  # Definindo o serializer para evitar o erro
    permission_classes = [IsAuthenticated]
    @extend_schema(
        summary="Deletar Conta do Usuário",
        description="Permite que o usuário autenticado delete sua própria conta.",
        responses={
            204: {"message": "Conta excluída com sucesso."},
            401: {"error": "Não autorizado. Token inválido ou expirado."}
        },
        tags=["Usuários"]
    )

    def delete(self, request, *args, **kwargs):
        user = self.request.user
        user.delete()
        return Response({"message": "Conta excluída com sucesso."}, status=204)
    
class RegisterUserView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        request=UserSerializer,
        responses={201: UserSerializer},
        description="Endpoint para registrar um novo usuário",
        summary="Registrar usuário",
        tags=["Usuários"],
    )
    def post(self, request):
        role = request.data.get("role")

        if role not in ["student", "teacher", "coordinator"]:
            return Response({"error": "Role inválido"}, status=status.HTTP_400_BAD_REQUEST)

        serializer_class = StudentSerializer if role == "student" else UserSerializer
        serializer = serializer_class(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            user.set_password(request.data["password"])  # Criptografa a senha corretamente
            user.save()
            return Response({"message": "Usuário cadastrado com sucesso", "user": serializer.data}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegisterTeacherView(APIView):
    """
    🔹 Apenas coordenadores podem criar professores.
    """
    permission_classes = [permissions.IsAuthenticated, IsCoordinator]

    @extend_schema(
        request=TeacherSerializer,
        responses={201: TeacherSerializer},
        description="Permite que apenas coordenadores registrem professores.",
        summary="Registrar professor",
        tags=["Usuários"],
    )
    def post(self, request):
        """Registra um professor usando TeacherSerializer."""
        serializer = TeacherSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {"message": "Professor cadastrado com sucesso!", "user": serializer.data},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegisterCoordinatorView(APIView):
    permission_classes = [permissions.IsAdminUser]  # Apenas superusuários podem acessar

    @extend_schema(
        request=UserSerializer,
        responses={201: UserSerializer},
        description="Permite que apenas superusuários registrem coordenadores.",
        summary="Registrar coordenador",
        tags=["Usuários"],
    )
    def post(self, request):
        data = request.data.copy()
        data["role"] = "coordinator"  # Força a role

        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(data["password"])  # 🔹 Criptografa a senha corretamente
            user.save()
            return Response({"message": "Coordenador cadastrado com sucesso!", "user": serializer.data}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StudentDashboardView(GenericAPIView):
    permission_classes = [IsAuthenticated, IsStudent]
    serializer_class = DashboardSerializer

    def get(self, request):
        data = {"message": "Bem-vindo ao painel do aluno!"}
        serializer = self.get_serializer(data)
        return Response(serializer.data)

class TeacherDashboardView(GenericAPIView):
    permission_classes = [IsAuthenticated, IsTeacher]
    serializer_class = DashboardSerializer

    def get(self, request):
        data = {"message": "Bem-vindo ao painel do professor!"}
        serializer = self.get_serializer(data)
        return Response(serializer.data)

class CoordinatorDashboardView(GenericAPIView):
    permission_classes = [IsAuthenticated, IsCoordinator]
    serializer_class = DashboardSerializer

    def get(self, request):
        data = {"message": "Bem-vindo ao painel do coordenador!"}
        serializer = self.get_serializer(data)
        return Response(serializer.data)
    
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer