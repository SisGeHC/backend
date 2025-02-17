from django.urls import path

from .views import (
    DateCreateView,
    DateListView,
    EventCreateView,
    EventDetailView,
    EventListView,
    StudentEnrolledEventsView,
    EventUpdateView,
    DateUpdateView,
    EventDeleteView,
    ProfessorCreatedEventsView,
)

urlpatterns = [
    path("dates/create/", DateCreateView.as_view(), name="date-create"),
    path("dates/", DateListView.as_view(), name="date-list"),
    path("list/", EventListView.as_view(), name="event-list"),
    path("create/", EventCreateView.as_view(), name="event-create"),
    path("<int:pk>/", EventDetailView.as_view(), name="event-detail"),
    path("<int:id>/update/", EventUpdateView.as_view(), name="event-update"),
    path("dates/<int:id>/update/", DateUpdateView.as_view(), name="date-update"),
    path("<int:id>/delete/", EventDeleteView.as_view(), name="event-delete"),
    path(
        "student/<int:student_id>/enrolled/",
        StudentEnrolledEventsView.as_view(),
        name="student-enrolled-events",
    ),
    path(
        "professor/<int:professor_id>/created/", 
        ProfessorCreatedEventsView.as_view(), 
        name="professor-created-events"),
]
