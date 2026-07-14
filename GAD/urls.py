from django.urls import path
from . import views

urlpatterns=[
    path('GAD/',views.rbim,name='rbim'),
    # path('GAD/SOCIAL SECTOR',views.social_sector,name='social_sector')
]