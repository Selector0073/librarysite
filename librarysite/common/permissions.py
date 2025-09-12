from rest_framework.permissions import BasePermission
from user.models import User
from rest_framework import permissions


        
class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.admin is True
        )



class IsLogged(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)
