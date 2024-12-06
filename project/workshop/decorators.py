from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def role_required(allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.error(request, 'Debe iniciar sesión para acceder a esta página.')
                return redirect('login')
            
            # Superuser always has access
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            
            try:
                user_profile = request.user.userprofile
                # Convert allowed_roles to list if it's a string
                roles = [allowed_roles] if isinstance(allowed_roles, str) else allowed_roles
                # Add 'admin' to allowed roles if not already included
                if 'admin' not in roles:
                    roles.append('admin')
                # Add 'receptionist' to allowed roles for client and reservation management
                if any(role in ['client_management', 'reservation_management'] for role in roles):
                    roles.append('receptionist')
                # Check if user's role is in allowed roles
                if user_profile.role in roles or user_profile.role == 'receptionist':
                    return view_func(request, *args, **kwargs)
            except:
                pass
            
            raise PermissionDenied('No tiene permisos para acceder a esta página.')
        return _wrapped_view
    return decorator

def admin_required(view_func):
    return role_required(['admin'])(view_func)

def mechanic_required(view_func):
    return role_required(['mechanic'])(view_func)

def receptionist_required(view_func):
    return role_required(['admin', 'receptionist'])(view_func)

def client_management_required(view_func):
    return role_required(['admin', 'receptionist'])(view_func)

def reservation_management_required(view_func):
    return role_required(['admin', 'receptionist'])(view_func)