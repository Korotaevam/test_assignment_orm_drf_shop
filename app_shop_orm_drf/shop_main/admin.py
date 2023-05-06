from django.contrib import admin

from .models import *


# Register your models here.

class ShopAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('id',)


admin.site.register(ShopModels, ShopAdmin)
admin.site.register(CityModels, ShopAdmin)
admin.site.register(StreetModels, ShopAdmin)
