from rest_framework.permissions import BasePermission

class IsCompanyLead(BasePermission):
    message = "You have not permission for entering corporate board. Please try to enter user board or get permission"
    def has_permission(self, request, view):
        return bool(request.user and request.user.employee.is_systemadmin == True)
    
    

    
    