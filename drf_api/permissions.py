from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS, BasePermission

class IsEmployer(permissions.BasePermission):
    """
    Pozwala na dostęp CRUD tylko zalogowanym użytkownikom, którzy są pracodawcami.
    """
    
    def has_permission(self, request, view):
        # Sprawdź, czy użytkownik jest zalogowany
        if not request.user or not request.user.is_authenticated:
            return False
        # Pozwala na dostęp tylko pracodawcom
        return request.user.is_employer

    def has_object_permission(self, request, view, obj):
        # Użytkownik może widzieć/edytować/usuwać tylko obiekty związane z jego firmą
        return request.user.is_authenticated and request.user.is_employer

class IsEmployeeReadOnly(permissions.BasePermission):
    """
    Pozwala na dostęp do odczytu dla wszystkich zalogowanych użytkowników, ale blokuje operacje zapisu.
    """
    
    def has_permission(self, request, view):
        # Sprawdź, czy użytkownik jest zalogowany i nie jest pracodawcą
        if request.user and request.user.is_authenticated:
            return request.method in permissions.SAFE_METHODS or not request.user.is_employer
        return False


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS