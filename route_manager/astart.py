import heapq
from .utils import get_heuristic


def reconstruct_path(came_from, current):
    path = [current]

    while current in came_from:
        current = came_from[current]
        path.append(current)

    path.reverse()
    return path


def astar(graph, start, end):
    open_set = []

    heapq.heappush(
        open_set,
        (get_heuristic(start), start)
    )

    came_from = {}

    g_score = {
        start: 0
    }

    f_score = {
        start: get_heuristic(start)
    }

    while open_set:

        _, current = heapq.heappop(open_set)

        if current == end:
            return {
                "path": reconstruct_path(
                    came_from,
                    current
                ),
                "cost": g_score[current]
            }

        for neighbour, distance in graph.get(current, []):

            tentative_g = (
                g_score[current]
                + distance
            )

            if (
                neighbour not in g_score
                or tentative_g < g_score[neighbour]
            ):

                came_from[neighbour] = current

                g_score[neighbour] = tentative_g

                h = get_heuristic(neighbour)

                f = tentative_g + h

                f_score[neighbour] = f

                heapq.heappush(
                    open_set,
                    (f, neighbour)
                )

    return None