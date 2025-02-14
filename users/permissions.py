from rest_framework import permissions

from rest_framework.permissions import BasePermission

class IsTeacherOrCoordinator(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ["teacher", "coordinator"]

class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "student"

class IsEventCreator(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and obj.created_by == request.user
    
class IsTeacher(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "teacher"
    
class IsCoordinator(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "coordinator"