from rest_framework import permissions


class LoggedInPermission(permissions.BasePermission):
    """User must be logged in"""

    def has_permission(self, request, view):
        return request.user.id is not None


class IsStaff(permissions.BasePermission):
    """User must be coach of staff in"""

    def has_permission(self, request, view):
        return request.user.is_staff


class UserViewsPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == "PUT" or request.method == "GET":
            return request.user.id is not None
        return True


class CoachOfNote(permissions.BasePermission):
    """same id of coach note"""

    def has_permission(self, request, view):
        if request.data.get("coach") != None:
            return int(request.data.get("coach")) == request.user.id

        else:
            return True
