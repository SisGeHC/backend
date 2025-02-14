from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)

from .models import Professor
from .serializers import ProfessorCreateSerializer, ProfessorSerializer


class ProfessorCreateView(CreateAPIView):
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
