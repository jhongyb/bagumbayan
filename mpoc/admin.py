from django.contrib import admin
from .models import ExecutiveOrder,Ordinance,Incident

class EOAdmin(admin.ModelAdmin):
    list_display=['eo_date','eo_title','eo_number']

class OrdinanceAdmin(admin.ModelAdmin):
    list_display=['ordinance_date','ordinance_title','ordinance_number']

admin.site.register(ExecutiveOrder,EOAdmin)
admin.site.register(Ordinance,OrdinanceAdmin)
admin.site.register(Incident)
