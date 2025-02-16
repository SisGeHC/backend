from django.urls import path

from .views import (
    DateCreateView,
    DateListView,
    EventCreateView,
    EventDetailView,
    EventListView,
)

urlpatterns = [
    path("dates/create/", DateCreateView.as_view(), name="date-create"),
    path("dates/", DateListView.as_view(), name="date-list"),
    path("list/", EventListView.as_view(), name="event-list"),
    path("create/", EventCreateView.as_view(), name="event-create"),
    path("<int:pk>/", EventDetailView.as_view(), name="event-detail"),
]
