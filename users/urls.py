from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import LogoutView
from .views import RegisterUserView, UpdateUserView, DeleteUserView

router = DefaultRouter()


urlpatterns = [
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/register/', RegisterUserView.as_view(), name='user_register'),
    path('users/<int:pk>/update/', UpdateUserView.as_view(), name='user_update'),
    path('users/<int:pk>/delete/', DeleteUserView.as_view(), name='user_delete'),
    path('auth/logout/', LogoutView.as_view(), name='token_logout'),
    path('', include(router.urls)),
]
