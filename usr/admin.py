from django.contrib import admin
from .models import ViewAccess,Page,Barangay


class ViewAccessAdmin(admin.ModelAdmin):
    list_display=['user','page']

admin.site.register(ViewAccess,ViewAccessAdmin)
admin.site.register(Page)
admin.site.register(Barangay)
