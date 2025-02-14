from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)

from .models import Coordinator
from .serializers import CoordinatorCreateSerializer, CoordinatorSerializer


class CoordinatorCreateView(CreateAPIView):
    queryset = Coordinator.objects.all()
    serializer_class = CoordinatorCreateSerializer


class CoordinatorListView(ListAPIView):
    queryset = Coordinator.objects.all()
    serializer_class = CoordinatorSerializer


class CoordinatorDetailView(RetrieveAPIView):
    queryset = Coordinator.objects.all()
    serializer_class = CoordinatorSerializer


class CoordinatorUpdateView(UpdateAPIView):
    queryset = Coordinator.objects.all()
    serializer_class = CoordinatorSerializer
    http_method_names = ["patch"]
