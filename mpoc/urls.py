from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns=[
#executive order
path('mpoc/',views.mpoc_home,name='mpoc_home'),
path('mpoc/eo/',views.mpoc_eo,name='mpoc_eo'),
path('mpoc/eo/new',views.mpoc_neweo,name='mpoc_neweo'),
path('mpoc/eo/<pk>update',views.mpoc_updateeo,name='mpoc_updateeo'),
path('mpoc/eo/<pk>download',views.mpoc_downloadeo,name='mpoc_downloadeo'),
path('mpoc/eo/<pk>Removed',views.mpoc_deleteeo,name='mpoc_deleteeo'),
#ordinance
path('mpoc/ordinance',views.mpoc_ordinance,name='mpoc_ordinance'),
path('mpoc/ordinance/new',views.mpoc_newordinance,name='mpoc_newordinance'),
path('mpoc/ordinance/<pk>update',views.mpoc_updateordinance,name='mpoc_updateordinance'),
path('mpoc/ordinance/<pk>download',views.mpoc_downloadordinance,name='mpoc_downloadordinance'),
path('mpoc/ordinance/<pk>Removed',views.mpoc_deleteordinance,name='mpoc_deleteordinance'),

#INCIDENT
path('mpoc/incident',views.mpoc_incident,name='mpoc_incident'),
path('mpoc/incident/new',views.mpoc_newincident,name='mpoc_newincident'),
path('mpoc/incident/<pk>update',views.mpoc_updateincidents,name='mpoc_updateincident'),
path('mpoc/incident/<pk>download',views.mpoc_downloadincident,name='mpoc_downloadincident'),
path('mpoc/incident/<pk>Removed',views.mpoc_deleteincident,name='mpoc_deleteincident'),




]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)