from django.shortcuts import render
from django.http import JsonResponse
from django.views import View

from .models import Shop
# Create your views here.
def index(request):
    # templates/index.html exists at project root templates/, so render that
    return render(request, 'index.html')

class ShopListJsonView(View):
    def get(self, request, *args, **kwargs):
        shops = list(Shop.objects.values(
            "id",
            "name",
            "lat",
            "lng",
            "garbage_weight",
            "is_active",
        ))
        return JsonResponse(shops, safe=False) 