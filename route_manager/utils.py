from .models import Shop, Edge


def build_graph():
    graph = {
        shop.id: []
        for shop in Shop.objects.filter(is_active=True)
    }
    edges = Edge.objects.select_related(
        "from_shop",
        "to_shop"
    )

    for edge in edges:
        graph[edge.from_shop.id].append(
            (edge.to_shop.id, edge.distance_km)
        )
    return graph


def get_heuristic(shop_id):
    try:
        shop = Shop.objects.get(id = shop_id)
        return shop.garbage_weight
    except Shop.DoesNotExist:
        return 0.0
