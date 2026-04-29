from .models import ViewAccess
from django.contrib import messages

def ViewDtr(user):
    return user.username in ['admin','jhong']

def ViewEmployee(user):
    lst=ViewAccess.objects.filter(page=2).all().values_list('user__username',flat=True)
    return user.username in list(lst)

def mpoc_access(user):
    lst=ViewAccess.objects.filter(page=1).all().values_list('user__username',flat=True)
    return user.username in list(lst)
