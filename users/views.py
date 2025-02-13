from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from drf_spectacular.utils import extend_schema
from .serializers import UserSerializer
from django.contrib.auth.hashers import make_password
## users/views.py
from rest_framework import permissions
from django.shortcuts import get_object_or_404
from .models import User
from .serializers import UserSerializer

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()  # Invalida o token
            return Response({"message": "Logout realizado com sucesso!"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class RegisterUserView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """Cria um novo usuário sem necessidade de autenticação."""
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Usuário cadastrado com sucesso', 'user': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdateUserView(APIView):
    permission_classes = []

    def patch(self, request, pk):
        """Permite que o usuário edite apenas o próprio perfil."""
        user = get_object_or_404(User, pk=pk)
        if request.user != user and not request.user.is_staff:
            return Response({'error': 'Você não tem permissão para editar este perfil.'}, status=status.HTTP_403_FORBIDDEN)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Perfil atualizado com sucesso', 'user': serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk):
        """Permite que um usuário exclua apenas a própria conta."""
        user = get_object_or_404(User, pk=pk)
        if request.user != user and not request.user.is_staff:
            return Response({'error': 'Você não tem permissão para deletar esta conta.'}, status=status.HTTP_403_FORBIDDEN)
        user.delete()
        return Response({'message': 'Conta deletada com sucesso'}, status=status.HTTP_204_NO_CONTENT)
    
class RegisterUserView(APIView):
    permission_classes = []

    @extend_schema(
        request=UserSerializer,
        responses={201: UserSerializer},
        description="Endpoint para registrar um novo usuário",
        summary="Registrar usuário",
        tags=["Usuários"],
    )
    def post(self, request):
        """Cria um novo usuário sem necessidade de autenticação."""
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(password=make_password(request.data['password']))
            return Response({'message': 'Usuário cadastrado com sucesso', 'user': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)