from rest_framework.permissions import BasePermission
from user.models import User
from rest_framework import permissions
from .PasswordResetRequired import PasswordResetRequired



class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if not PasswordResetRequired().has_permission(request, view):
            return False
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.is_admin
        )



class IsLogged(BasePermission):
    def has_permission(self, request, view):
        if not PasswordResetRequired().has_permission(request, view):
            return False
        return bool(
            request.user 
            and request.user.is_authenticated
        )



class CanChangePassword(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        if getattr(view, "allow_password_change_for_reset", False):
            return True
        return not getattr(user, "password_need_reset", False)
