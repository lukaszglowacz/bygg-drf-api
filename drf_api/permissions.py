from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user
    
    
class IsEmployeeOrReadOnly(permissions.BasePermission):

    #Uprawnienia pozwala na operacje zapisu jedynie dla pracownikow
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and (not request.user.is_employer))
    

class IsEmployer(permissions.BasePermission):

    #Uprawnienia pozwalaja na CRUD jedynie dla pracodawcow
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_employer)
