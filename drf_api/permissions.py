from rest_framework import permissions

class IsEmployee(permissions.BasePermission):
    """
    Pozwala na dostęp tylko zalogowanym użytkownikom, którzy nie są pracodawcami.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and not request.user.is_employer)

    def has_object_permission(self, request, view, obj):
        # Użytkownik może zobaczyć tylko swoje dane.
        return obj.user == request.user

class IsEmployer(permissions.BasePermission):
    """
    Pozwala na pełen dostęp CRUD tylko dla pracodawców.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_employer)

    def has_object_permission(self, request, view, obj):
        # Pracodawcy mają dostęp do wszystkich obiektów.
        return self.has_permission(request, view)

class WorkPlacePermissions(permissions.BasePermission):
    """
    Uprawnienia dla miejsc pracy. Pracownicy mogą tylko odczytywać, pracodawcy mają dostęp CRUD.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated and request.user.is_employer)

class WorkHourPermissions(permissions.BasePermission):
    """
    Uprawnienia dla godzin pracy. Pracownicy mogą tylko zapisywać swoje godziny pracy,
    nie mają możliwości ich edycji czy usuwania. Pracodawcy mają dostęp CRUD.
    """

    def has_permission(self, request, view):
        # Wszyscy zalogowani użytkownicy mogą dodawać godziny pracy (POST),
        # ale tylko pracodawcy mogą wykonywać inne operacje (PUT, DELETE).
        if request.method == 'POST':
            return bool(request.user and request.user.is_authenticated)
        else:
            return bool(request.user and request.user.is_authenticated and request.user.is_employer)

    def has_object_permission(self, request, view, obj):
        # Pracodawcy mają dostęp do wszystkich obiektów godzin pracy.
        # Pracownicy nie mają dostępu do edycji ani usuwania godzin pracy (ani swoich, ani innych).
        return request.user.is_employer


class IsOwnerOrEmployer(permissions.BasePermission):
    """
    Pozwala użytkownikowi modyfikować własny profil oraz pozwala pracodawcom na modyfikowanie dowolnego profilu.
    """
    def has_object_permission(self, request, view, obj):
        # Pracodawcy mogą edytować każdy profil
        if request.user.is_employer:
            return True
        # Użytkownicy mogą edytować tylko swój profil
        return obj.user == request.user
