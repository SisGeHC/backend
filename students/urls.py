from django.urls import path

from .views import (
    StudentCreateView,
    StudentDetailView,
    StudentListView,
    StudentUpdateView,
)

urlpatterns = [
    path("create", StudentCreateView.as_view(), name="student-create"),
    path("list", StudentListView.as_view(), name="student-list"),
    path("<int:pk>/update/", StudentUpdateView.as_view(), name="student-update"),
    path("<int:pk>/", StudentDetailView.as_view(), name="student-detail"),
]
