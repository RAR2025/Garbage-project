from django.contrib import admin
from .models import Shop, Edge

# Register your models here.

@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ("name", "garbage_weight", "is_active", "lat", "lng")
    list_filter = ("is_active",)
    search_fields =("name",)
    ordering =("name",)

@admin.register(Edge)
class EdgeAdmin(admin.ModelAdmin):
    list_display=("from_shop", "to_shop", "distance_km")
    list_filter=("distance_km",)
