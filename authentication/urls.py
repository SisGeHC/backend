from django.urls import path

from .views import ChangePasswordView, CustomAuthToken

urlpatterns = [
    path("api-token-auth/", CustomAuthToken.as_view(), name="api_token_auth"),
    path("change-password/", ChangePasswordView.as_view(), name="change-password"),
]
