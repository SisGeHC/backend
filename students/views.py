from rest_framework.generics import CreateAPIView, ListAPIView

from .models import Student
from .serializers import StudentCreateSerializer, StudentSerializer


class StudentCreateView(CreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentCreateSerializer


class StudentListView(ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
