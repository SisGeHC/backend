from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "swagger/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"
    ),
    path(f"api/api-auth/", include("rest_framework.urls")),
    path(f"api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        f"api/swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger",
    ),
    path("courses/", include("courses.urls")),
    path("students/", include("students.urls")),
    path("professors/", include("professors.urls")),
    path("coordinators/", include("coordinators.urls")),
    path("certificates/", include("certificates.urls")),
    path("authentication/", include("authentication.urls")),
    path("events/", include("events.urls")),
    path("enrollments/", include("enrollments.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)