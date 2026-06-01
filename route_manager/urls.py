from django.urls import path

from . import views




urlpatterns = [
    path('', views.index),
    path("shops/", views.ShopListJsonView.as_view(), name="shop-list")
]