from django.urls import path

from . import views




urlpatterns = [
    path('', views.map_view, name='map'),
    path("shops/", views.ShopListJsonView.as_view(), name="shop-list"),
    path("shops/<int:pk>/update_weight/", views.update_shop_weight, name="shop-update-weight"),
    path("edges/", views.EdgeListJsonView.as_view(), name="edge-list"),
    path("route/<int:start_id>/<int:end_id>/", views.compute_route, name="compute_route"),
]