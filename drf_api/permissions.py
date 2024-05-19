from rest_framework import permissions

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
        return request.user.is_employer and obj.employer == request.user

class IsEmployee(permissions.BasePermission):
    """
    Pozwala na dostęp tylko zalogowanym użytkownikom, którzy nie są pracodawcami.
    """
    
    def has_permission(self, request, view):
        # Sprawdź, czy użytkownik jest zalogowany
        if not request.user or not request.user.is_authenticated:
            return False
        # Pozwala na dostęp, jeśli nie są pracodawcami
        return not request.user.is_employer

    def has_object_permission(self, request, view, obj):
        # Użytkownik może zobaczyć tylko swoje dane
        return obj.user == request.user
