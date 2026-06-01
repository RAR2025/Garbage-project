from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .models import Shop, Edge
from .forms import ShopWeightForm
from django.shortcuts import get_object_or_404
import  json
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
    

@csrf_exempt
@require_POST
def update_shop_weight(request, pk):
    shop = get_object_or_404(Shop, pk=pk)

    if request.content_type == 'application/json':
        try:
            payload = json.loads(request.body.decode() or "{}")
        except json.JSONDecodeError:
            return JsonResponse({'errors': {"__all__": ["Invalid JSON"]}}, status=400)
    else:
        payload = request.POST.dict()

    form = ShopWeightForm(payload, instance=shop)
    if form.is_valid():
        form.save()
        return JsonResponse({"status" : "ok"})
    return JsonResponse({"errors": form.errors})

class EdgeListJsonView(View):
    def get(self, request, *args, **kwargs):
        edges = list(
            Edge.objects.select_related("from_shop", "to_shop").values(
                "id",
                "distance_km",
                "from_shop_id",
                "to_shop_id",
                "from_shop__name",
                "to_shop__name",
            )
        )
        return JsonResponse(edges, safe=False)