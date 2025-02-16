from rest_framework.generics import ListCreateAPIView

from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Course
from .serializers import CourseSerializer


class CourseListCreateView(ListCreateAPIView):

    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated()]
        
        

