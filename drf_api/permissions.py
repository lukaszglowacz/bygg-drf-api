from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS, BasePermission

class IsEmployer(permissions.BasePermission):
    """
    Custom permission to allow CRUD access only for authenticated users who are employers.
    """
    
    def has_permission(self, request, view):
        # Check if the user is authenticated
        if not request.user or not request.user.is_authenticated:
            return False  # Deny permission if user is not logged in
        # Allow access if the user is an employer
        return request.user.is_employer

    def has_object_permission(self, request, view, obj):
        # Additional permission check to ensure the user can view/modify/delete only objects associated with their own company
        return request.user.is_authenticated and request.user.is_employer


class ReadOnly(BasePermission):
    """
    Permission class to allow read-only access to any user.
    """
    def has_permission(self, request, view):
        # Allow permission if the HTTP method is one of the safe methods (GET, HEAD, OPTIONS)
        return request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        # Object-level permission check to allow read-only access to the objects
        return request.method in SAFE_METHODS
