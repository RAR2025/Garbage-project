from .astart import astar



def generate_priority_route(graph, start_node, shops):
    """
    Greedy garbage collection route.

    1. Sort shops by garbage weight descending.
    2. Run A* between consecutive locations.
    3. Return full path.

    NOTE:
    This is a greedy approximation and
    does NOT guarantee optimal TSP route.
    """

    ordered_shops = sorted(
        shops,
        key=lambda x: x["garbage_weight"],
        reverse=True
    )
    full_path = []
    total_cost = 0
    current = start_node

    for shop in ordered_shops:

        result = astar(
            graph,
            current,
            shop["id"]
        )

        if result:

            route_segment = result["path"]
            total_cost += result["cost"]

            if full_path:
                full_path.extend(route_segment[1:])
            else:
                full_path.extend(route_segment)

        current = shop["id"]

    # return to depot
    result = astar(
        graph,
        current,
        start_node
    )

    if result:
        total_cost += result["cost"]
        full_path.extend(result["path"][1:])

    return {
        "route": full_path,
        "total_cost": total_cost
    }