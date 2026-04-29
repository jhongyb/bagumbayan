from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns=[
path('mpoc/',views.mpoc_home,name='mpoc_home'),
path('mpoc/eo/',views.mpoc_eo,name='mpoc_eo'),
path('mpoc/eo/new',views.mpoc_neweo,name='mpoc_neweo'),
path('mpoc/eo/<pk>update',views.mpoc_updateeo,name='mpoc_updateeo'),
path('mpoc/eo/<pk>download',views.mpoc_downloadeo,name='mpoc_downloadeo')
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)