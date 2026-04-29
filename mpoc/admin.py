from django.contrib import admin
from .models import ExecutiveOrder

class EOAdmin(admin.ModelAdmin):
    list_display=['eo_date','eo_title','eo_number']

admin.site.register(ExecutiveOrder,EOAdmin)
