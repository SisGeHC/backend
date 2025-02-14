from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import (
    CertificateCreateView,
    CertificateListView,
    CertificatePreviewView,
    CertificateUpdateView,
)

urlpatterns = [
    path("", CertificateListView.as_view(), name="certificae-list"),
    path(
        "post/",
        CertificateCreateView.as_view(),
        name="certificate-create",
    ),
    path(
        "<int:pk>/preview/",
        CertificatePreviewView.as_view(),
        name="certificate-preview",
    ),
    path(
        "<int:pk>/update/", CertificateUpdateView.as_view(), name="certificate-update"
    ),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
