from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import AllowAny

from .models import Student
from .serializers import StudentCreateSerializer, StudentSerializer


class StudentCreateView(CreateAPIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    queryset = Student.objects.all()
    serializer_class = StudentCreateSerializer


class StudentListView(ListAPIView):

    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class StudentDetailView(RetrieveAPIView):

    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    lookup_field = "pk"


class StudentUpdateView(UpdateAPIView):

    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    lookup_field = "pk"
    http_method_names = ["patch"]
