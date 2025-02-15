from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import AllowAny

from .models import Coordinator
from .serializers import CoordinatorCreateSerializer, CoordinatorSerializer


class CoordinatorCreateView(CreateAPIView):
    authentication_classes = []
    permission_classes = [AllowAny]
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
