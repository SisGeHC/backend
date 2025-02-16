from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import AttendanceValidationView, EnrollmentViewSet

router = DefaultRouter()
router.register(r"", EnrollmentViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "validate-attendance/",
        AttendanceValidationView.as_view(),
        name="validate-attendance",
    ),
]
