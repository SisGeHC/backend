from django.urls import path

from .views import (
    DateCreateView,
    DateListView,
    EventCreateView,
    EventDetailView,
    EventListView,
    StudentEnrolledEventsView,
)

urlpatterns = [
    path("dates/create/", DateCreateView.as_view(), name="date-create"),
    path("dates/", DateListView.as_view(), name="date-list"),
    path("list/", EventListView.as_view(), name="event-list"),
    path("create/", EventCreateView.as_view(), name="event-create"),
    path("<int:pk>/", EventDetailView.as_view(), name="event-detail"),
    path(
        "student/<int:student_id>/enrolled/",
        StudentEnrolledEventsView.as_view(),
        name="student-enrolled-events",
    ),
]
