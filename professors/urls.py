from django.urls import path

from .views import (
    ProfessorCreateView,
    ProfessorDetailView,
    ProfessorListView,
    ProfessorUpdateView,
)

urlpatterns = [
    path("create", ProfessorCreateView.as_view(), name="professor-create"),
    path("list", ProfessorListView.as_view(), name="professor-list"),
    path("<int:pk>/update/", ProfessorUpdateView.as_view(), name="professor-update"),
    path("<int:pk>/", ProfessorDetailView.as_view(), name="professor-detail"),
]
