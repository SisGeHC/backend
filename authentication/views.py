from django.contrib.auth import update_session_auth_hash
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from coordinators.models import Coordinator
from professors.models import Professor
from students.models import Student

from .serializers import ChangePasswordSerializer, CustomAuthTokenSerializer


class CustomAuthToken(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)

        user_type = None
        if Student.objects.filter(user=user).exists():
            user_type = "student"
        elif Coordinator.objects.filter(user=user).exists():
            user_type = "coordinator"
        elif Professor.objects.filter(user=user).exists():
            user_type = "professor"

        return Response(
            {
                "token": token.key,
                "user_id": user.pk,
                "email": user.email,
                "username": user.username,
                "user_type": user_type,
            }
        )


class ChangePasswordView(APIView):
    serializer_class = ChangePasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data["new_password"])
            user.save()

            update_session_auth_hash(request, user)

            return Response(
                {"message": "Senha alterada com sucesso."}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
