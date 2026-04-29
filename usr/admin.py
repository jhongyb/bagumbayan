from django.contrib import admin
from .models import ViewAccess,Page


class ViewAccessAdmin(admin.ModelAdmin):
    list_display=['user','page']

admin.site.register(ViewAccess,ViewAccessAdmin)
admin.site.register(Page)
