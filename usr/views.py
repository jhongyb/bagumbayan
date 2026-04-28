from django.shortcuts import render
from .forms import UserLoginForm
from django.contrib.auth.decorators import login_required



@login_required
def Home(request):
    return render(request,'base.html')

@login_required
def Restricted(request):
    return render(request,'restricted.html')