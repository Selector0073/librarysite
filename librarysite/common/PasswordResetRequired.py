from rest_framework.permissions import BasePermission
from rest_framework import status
from rest_framework.exceptions import APIException

class PasswordResetRequiredException(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "Password reset is required."
    default_code = "password_reset_required"

class PasswordResetRequired(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user and user.is_authenticated:
            if getattr(user, 'password_need_reset', False):
                raise PasswordResetRequiredException()
        return True
