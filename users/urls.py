from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LoginView
from .views import RegisterUserView, UpdateUserView, DeleteUserView, RegisterTeacherView, RegisterCoordinatorView
from .views import StudentDashboardView, TeacherDashboardView, CoordinatorDashboardView, CurrentUserView
from rest_framework_simplejwt.views import TokenRefreshView, TokenBlacklistView

router = DefaultRouter()


urlpatterns = [
    path('', include(router.urls)),
    #auth
    path('auth/login/', LoginView.as_view(), name='token_obtain_pair'),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),  # Renova o token de acesso
    path("auth/logout/", TokenBlacklistView.as_view(), name="token_blacklist"),  # Invalida o refresh token

    #crud Users
    path('auth/register-coordinator/', RegisterCoordinatorView.as_view(), name='register_coordinator'),
    path('auth/register-teacher/', RegisterTeacherView.as_view(), name='register_teacher'),
    path("auth/register/", RegisterUserView.as_view(), name="user_register"),
    path('update/', UpdateUserView.as_view(), name='user_update'),
    path('users/<int:pk>/delete/', DeleteUserView.as_view(), name='user_delete'),
    path('me/', CurrentUserView.as_view(), name='user-detail'),

    #Controle de acesso de cada grupo
    path("students/dashboard/", StudentDashboardView.as_view(), name="student_dashboard"),
    path("teachers/dashboard/", TeacherDashboardView.as_view(), name="teacher_dashboard"),
    path("coordinators/dashboard/", CoordinatorDashboardView.as_view(), name="coordinator_dashboard"),
]
