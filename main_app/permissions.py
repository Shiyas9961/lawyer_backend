from rest_framework.permissions import BasePermission

# SuperAdim, Admin, User, Viewer (Optional)

class IsUserSuperAdmin(BasePermission) :
    def has_permission(self, request, view):
        if (not request.user) or (not request.user.is_authenticated) :
            return False

        return request.user.role in ['superadmin']

class IsAdminUser(BasePermission) :

    def has_permission(self, request, view):

        if (not request.user) or (not request.user.is_authenticated) :
            return False
        
        return request.user.role in ['superadmin', 'admin']
    
class IsUserUser(BasePermission) :

    def has_permission(self, request, view):

        if (not request.user) or (not request.user.is_authenticated) :
            return False
        
        return request.user.role in ['superadmin', 'admin', 'user']
    