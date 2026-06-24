from django.test import TestCase
from django.urls import reverse
from .models import Shop, Edge
from .utils import build_graph
from .astart import astar
import json

class AStarAlgorithmTests(TestCase):
    def setUp(self):
        self.shop1 = Shop.objects.create(name="Shop A", lat=0, lng=0, garbage_weight=10)
        self.shop2 = Shop.objects.create(name="Shop B", lat=1, lng=1, garbage_weight=50)
        self.shop3 = Shop.objects.create(name="Shop C", lat=2, lng=2, garbage_weight=20)
        self.shop4 = Shop.objects.create(name="Shop D (Disconnected)", lat=3, lng=3, garbage_weight=5)
        
        Edge.objects.create(from_shop=self.shop1, to_shop=self.shop2, distance_km=5.0)
        Edge.objects.create(from_shop=self.shop2, to_shop=self.shop3, distance_km=5.0)
        Edge.objects.create(from_shop=self.shop1, to_shop=self.shop3, distance_km=15.0)

    def test_correct_path_found(self):
        graph = build_graph()
        result = astar(graph, self.shop1.id, self.shop3.id)
        self.assertIsNotNone(result)
        self.assertEqual(result["path"], [self.shop1.id, self.shop2.id, self.shop3.id])
        self.assertEqual(result["cost"], 10.0)

    def test_disconnected_graph_handled(self):
        graph = build_graph()
        result = astar(graph, self.shop1.id, self.shop4.id)
        self.assertIsNone(result)

class APIViewTests(TestCase):
    def setUp(self):
        self.shop = Shop.objects.create(name="Test Shop", lat=19.0, lng=72.0, garbage_weight=15.0)

    def test_shop_list_api(self):
        response = self.client.get(reverse('shop-list'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(len(data) > 0)
        self.assertEqual(data[0]['name'], "Test Shop")

    def test_update_shop_weight_valid(self):
        url = reverse('shop-update-weight', args=[self.shop.id])
        payload = {'garbage_weight': 25.5}
        response = self.client.post(url, json.dumps(payload), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "ok")
        self.shop.refresh_from_db()
        self.assertEqual(self.shop.garbage_weight, 25.5)

    def test_update_shop_weight_invalid_json(self):
        url = reverse('shop-update-weight', args=[self.shop.id])
        response = self.client.post(url, "{invalid-json}", content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("errors", response.json())