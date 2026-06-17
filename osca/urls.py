from django.urls import path
from . import views


urlpatterns=[
    path('OSCA/',views.osca,name='osca'),
    path('OSCA/NEW',views.newosca,name='newosca'),
    path('OSCA/MASTERLIST',views.oscamasterlist,name='oscamasterlist'),
    path('OSCA/UPDATE/r<pk>f',views.updatesenior,name='updatesenior'),
    path('OSCA/DELETE/r<pk>f',views.deletesenior,name='deletesenior')
]