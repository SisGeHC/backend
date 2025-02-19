from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    AttendanceValidationView,
    EnrollmentViewSet,
    SendEventNotificationView,
)

router = DefaultRouter()
router.register(r"", EnrollmentViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "validate-attendance/<int:enrollment_id>/",
        AttendanceValidationView.as_view(),
        name="validate-attendance",
    ),
    path(
        "send-event-notification/<int:event_id>/",
        SendEventNotificationView.as_view(),
        name="send-event-notification",
    ),
]
