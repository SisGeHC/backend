from django.urls import path

from .views import (
    CoordinatorCreateView,
    CoordinatorDetailView,
    CoordinatorListView,
    CoordinatorUpdateView,
)

urlpatterns = [
    path("create", CoordinatorCreateView.as_view(), name="coordinator-create"),
    path("list", CoordinatorListView.as_view(), name="coordinator-list"),
    path("update", CoordinatorUpdateView.as_view(), name="coordinator-update"),
    path("<int:pk>/", CoordinatorDetailView.as_view(), name="coordinator-detail"),
]
