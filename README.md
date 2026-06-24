# Garbage Route Optimizer

Garbage Route Optimizer is a Django-based system that uses A* search to plan the optimal route for collecting garbage across various shop locations in a city.

## Running Locally

1. Setup virtual environment:
   ```powershell
   venv\Scripts\Activate.ps1
   ```
2. Run migrations (already applied to SQLite db):
   ```powershell
   python manage.py migrate
   ```
3. Run the development server:
   ```powershell
   python manage.py runserver
   ```
4. Access the application at `http://127.0.0.1:8000/`.

## Algorithm Explanation (A*)

The core route planning algorithm uses **A* search**.
Our goal is to prioritize the collection of garbage from shops that have the highest accumulated garbage weight. Therefore, the **heuristic** chosen for the A* search is the `garbage_weight` of a shop.
While typical A* implementations for routing use distance as a heuristic to find the shortest path, we use garbage weight because we want the pathfinder to greedily select nodes with higher garbage levels, maximizing the immediate collection volume.
*Note: Using a non-distance heuristic means the A* algorithm is not strictly admissible for shortest-distance paths, but rather acts as a priority-driven search to collect the most garbage early in the route.*

## API Endpoints

- `GET /api/shops/`
  Returns a list of all active shops with their current garbage weight and coordinates.
- `GET /api/edges/`
  Returns all the path connections (edges) between shops along with distances.
- `POST /api/shops/<id>/update_weight/`
  Updates the garbage weight for a given shop. Accepts JSON: `{"garbage_weight": 25.5}`.
- `GET /api/route/`
  Computes and returns the ordered list of shop IDs forming the collection route and the `total_distance`.

## Seeding Shops

To populate the database with initial shops and edges, use the custom management command:
```powershell
python manage.py seed_shops
```
