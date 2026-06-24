from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .models import Shop, Edge
from .forms import ShopWeightForm
from django.shortcuts import get_object_or_404
import  json
from .utils import build_graph
from .astart import astar
from .route_planner import generate_priority_route



def map_view(request):
    return render(request, "map.html")

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
                "from_shop__lat",
                "from_shop__lng",
                "to_shop__lat",
                "to_shop__lng",
            )
        )
        return JsonResponse(edges, safe=False)
    

def compute_route(request, start_id, end_id):
    graph = build_graph()
    result = astar(
        graph, start_id, end_id
    )

    if result is None:
        return JsonResponse(
            {
                "error": "no route found",
                "route": [],
                "total_distance": None
            },
            status = 404
        )

    return JsonResponse({
        "route": result["path"],
        "total_distance": result["cost"]
    })

def compute_full_route(request):
    graph = build_graph()
    shops = list(Shop.objects.filter(is_active=True).values("id", "garbage_weight"))
    
    # Assuming start_node is the first shop or id 1
    start_node = shops[0]["id"] if shops else 1
    
    result = generate_priority_route(graph, start_node, shops)
    
    return JsonResponse({
        "route": result["route"],
        "total_distance": result["total_cost"]
    })