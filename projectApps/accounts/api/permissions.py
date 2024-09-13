from rest_framework.permissions import BasePermission


class IsAuthenticatedAndOwner(BasePermission):
    message = "You do not have permission to perform this action."

    def has_permission(self, request, view):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            self.message = "You must be authenticated to perform this action."
            return False

        # Check if the user is active
        if not request.user.is_active:
            self.message = "User Not Found."
            return False

        return True
