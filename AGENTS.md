# AGENTS.md — Garbage Route Optimizer

## Quick start

```powershell
venv\Scripts\Activate.ps1
python manage.py runserver
```

Settings in `config/settings.py` — Django 6.0.5, SQLite, DEBUG=True.

## Virtual environment

`venv/` exists. No `requirements.txt`. If adding dependencies, create one: `pip freeze > requirements.txt`.

## Architecture

- **Single app** `route_manager/` with models `Shop` (lat/lng/garbage_weight/is_active) and `Edge` (directed weighted graph).
- **Entrypoints**: `manage.py`, `config/wsgi.py`, `config/asgi.py`.
- **Templates** at project root `templates/` (not app-level).
- **URLs**:
  | Path | View |
  |---|---|
  | `/` | `index.html` |
  | `/shops/` | `ShopListJsonView` (GET) |
  | `/shops/<pk>/update_weight/` | `update_shop_weight` (POST, `@csrf_exempt`) |
  | `/edges/` | `EdgeListJsonView` (GET) |
  | `/admin/` | Django admin |

## Core algorithm

- **A\* search** in `route_manager/astart.py` (note: filename is `astart`, not `astar`). Heuristic = `garbage_weight` (not distance).
- **Greedy multi-stop route planner** in `route_planner.py` — sorts shops by weight descending, runs A\* between consecutive stops, returns to start node.

## Key quirks

- `update_shop_weight` is `@csrf_exempt` by design; accepts both `application/json` and form-urlencoded.
- No lint/formatter/typechecker config exists yet.
- `tests.py` is a skeleton with no tests.
- No git remote configured; local-only repo.
- Migrations (3) already applied to `db.sqlite3`.
