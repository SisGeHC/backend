from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import AllowAny

from .models import Professor
from .serializers import ProfessorCreateSerializer, ProfessorSerializer


class ProfessorCreateView(CreateAPIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    queryset = Professor.objects.all()
    serializer_class = ProfessorCreateSerializer


class ProfessorListView(ListAPIView):

    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer


class ProfessorDetailView(RetrieveAPIView):

    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer


class ProfessorUpdateView(UpdateAPIView):

    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer
    http_method_names = ["patch"]
    lookup_field = "pk"
