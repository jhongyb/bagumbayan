
from django.contrib import admin
from . models import Osca_Informations,OscaCategory,OscaStatus



admin.site.register(OscaCategory)
admin.site.register(OscaStatus)

admin.site.register(Osca_Informations)