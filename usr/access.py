from .models import ViewAccess
from django.contrib import messages
from django.http import request
from django.shortcuts import redirect
from functools import wraps

def ViewDtr(user):
    return user.username in ['admin','jhong']

def restrict_employee(message="Not Authorized", redirect_url="/home"):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            lst = ViewAccess.objects.filter(page=2).values_list('user__username', flat=True)
            if request.user.username in list(lst):
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, message)
                return redirect(redirect_url)
        return _wrapped_view
    return decorator

def restrict_mpoc(message="Not Authorized", redirect_url="/home"):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            lst = ViewAccess.objects.filter(page=1).values_list('user__username', flat=True)
            if request.user.username in list(lst):
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, message)
                return redirect(redirect_url)
        return _wrapped_view
    return decorator