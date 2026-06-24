# Garbage Route Optimizer

A Django-based garbage collection route optimization system that uses the **A* Search Algorithm** to plan efficient garbage collection routes across multiple shop locations in a city.

The system maintains a network of shops and connecting roads, tracks garbage accumulation at each location, and generates optimized collection routes based on garbage priorities.

---

## Features

* Route optimization using A* Search
* Dynamic garbage weight tracking for shops
* REST API for shop, route, and edge management
* SQLite database support
* Automatic shop and route seeding
* Distance calculation between connected locations
* Priority-based garbage collection planning

---

## Tech Stack

* **Backend:** Django
* **Database:** SQLite
* **Algorithm:** A* Search
---

## Project Setup

### 1. Clone the Repository

```bash
git clone https://github.com/RAR2025/Garbage-project.git
cd Garbage-project
```

### 2. Create and Activate Virtual Environment

#### Windows (PowerShell)

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

#### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install django
```

### 4. Apply Database Migrations

```bash
python manage.py migrate
```

### 5. Seed Initial Shop Data

```bash
python manage.py seed_shops
```

### 6. Run the Development Server

```bash
python manage.py runserver
```

The application will be available at:

```text
http://127.0.0.1:8000/
```

---

## A* Search Algorithm

The core route planning functionality is powered by the **A* Search Algorithm**.

### Objective

The primary objective is to maximize garbage collection efficiency by prioritizing shops with higher accumulated garbage levels.

### Heuristic Used

Instead of using only geographical distance as the heuristic, this implementation uses the **garbage weight** of each shop.

```text
Heuristic = garbage_weight
```

This approach encourages the search algorithm to prioritize locations that contain larger amounts of garbage, ensuring that high-priority collection points are serviced earlier.

### Important Note

Traditional A* implementations use admissible heuristics such as straight-line distance to guarantee the shortest path.

In this project:

* Garbage weight is used as a priority heuristic.
* The algorithm favors high-value collection points.
* Route selection is optimized for collection priority rather than purely minimizing travel distance.

As a result, the search behaves as a hybrid between route optimization and priority-based resource collection.

---

## API Endpoints

### Get All Shops

```http
GET /api/shops/
```

Returns all active shops along with:

* Shop ID
* Name
* Coordinates
* Garbage Weight

---

### Get All Edges

```http
GET /api/edges/
```

Returns all path connections between shops and their associated distances.

---

### Update Garbage Weight

```http
POST /api/shops/<id>/update_weight/
```

#### Request Body

```json
{
  "garbage_weight": 25.5
}
```

Updates the garbage weight of a specific shop.

---

### Generate Collection Route

```http
GET /api/route/
```

Returns:

```json
{
  "route": [1, 5, 3, 7],
  "total_distance": 12.4
}
```

The route contains the ordered sequence of shop IDs selected by the optimizer.

---

## Database Seeding

To populate the database with sample shops and path connections:

```bash
python manage.py seed_shops
```

This command creates:

* Shop locations
* Road connections (edges)
* Initial garbage weights

---

## Project Structure

```text
Garbage-project/
│
├── manage.py
├── db.sqlite3
├── requirements.txt
│
├── app/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── serializers.py
│   └── algorithms/
│       └── astar.py
│
├── templates/
├── static/
└── README.md
```

---

## Future Improvements

* Real-time garbage monitoring
* Vehicle capacity constraints
* Traffic-aware route optimization
* GIS map integration
* Multi-vehicle route planning
* Predictive garbage accumulation using machine learning

---

## License

This project is intended for educational and research purposes.

---

Made with ❤️ by **Ruturaj Rajwade**
