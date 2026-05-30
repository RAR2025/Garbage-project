from django.contrib import admin
from .models import Shop, Edge

class EdgeInline(admin.TabularInline):
    model = Edge
    fk_name = "from_shop"
    extra = 0
    fields = ("to_shop", "distance_km")


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ("name", "garbage_weight", "is_active", "lat", "lng")
    list_filter = ("is_active",)
    search_fields = ("name",)
    ordering = ("name",)
    inlines = (EdgeInline,)

@admin.register(Edge)
class EdgeAdmin(admin.ModelAdmin):
    list_display = ("from_shop", "to_shop", "distance_km")
    list_filter = ("from_shop", "to_shop")
    search_fields = ("from_shop__name", "to_shop__name")
