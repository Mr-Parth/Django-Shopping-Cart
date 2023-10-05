from rest_framework import permissions

class IsAdminUserProfile(permissions.BasePermission):
    """
    Custom permission to check if the user's UserProfile role is 'admin'.
    """

    def has_permission(self, request, view):
        # Check if the user is authenticated
        if request.user.is_authenticated:
            # Check if the user's UserProfile role is 'admin'
            return request.user.userprofile.role == 'admin'
        return False