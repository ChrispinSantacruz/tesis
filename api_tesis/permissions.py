# api_tesis/permissions.py
from rest_framework.permissions import BasePermission

class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='students').exists()

class IsTeacher(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='teachers').exists()
