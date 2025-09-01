from rest_framework.permissions import BasePermission
from user.models import User

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        try:
            username = request.data.get('user')
            user = User.objects.get(username=username)
            return user.admin is True
        except User.DoesNotExist:
            return False

class IsLogged(BasePermission):
    def has_permission(self, request, view):
        # ! If user is logged in
        # ? JWT doesnt work
        return True