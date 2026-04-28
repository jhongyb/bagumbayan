from .import views
from django.urls import path
from django.contrib.auth import views as auth_views
from usr.forms import UserLoginForm

urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name='login.html',authentication_form=UserLoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('home/',views.Home,name='home'),
    path('restricted/',views.Home,name='restricted')
]