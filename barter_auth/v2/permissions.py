from rest_framework import permissions

class UserPermissions(permissions.BasePermission):
    safe_methods = ['OPTIONS', 'HEAD']

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser or request.user.is_staff:
            return True
        
        if request.method in self.safe_methods:
            return True
        
        if obj == request.user:
            return True
        
        return False