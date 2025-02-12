from django.urls import path

from .views import StudentCreateView, StudentListView

urlpatterns = [
    path("create", StudentCreateView.as_view(), name="student-create"),
    path("list", StudentListView.as_view(), name="student-list"),
]
