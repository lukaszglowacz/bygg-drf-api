from rest_framework import permissions



class IsOwnerOrEmployer(permissions.BasePermission):
    """
    Pozwala na pełen dostęp CRUD tylko dla pracodawców oraz właścicieli profilu,
    wymagając jednocześnie, aby byli zalogowani.
    """
    
    def has_permission(self, request, view):
        # Sprawdź, czy użytkownik jest zalogowany
        if not request.user or not request.user.is_authenticated:
            return False
        # Pracodawcy mają dostęp do wszystkich obiektów
        if request.user.is_employer:
            return True
        # Sprawdzenie dodatkowych warunków specyficznych dla widoku może być tutaj
        return super().has_permission(request, view)

    def has_object_permission(self, request, view, obj):
        # Użytkownik może widzieć/edytować/usuwać tylko własny profil
        return obj.user == request.user or request.user.is_employer
     

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