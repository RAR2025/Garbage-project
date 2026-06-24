from django.core.management.base import BaseCommand
from route_manager.models import Shop, Edge
import random

class Command(BaseCommand):
    help = 'Seeds the database with initial shops and edges'

    def handle(self, *args, **kwargs):
        self.stdout.write('Clearing existing data...')
        Edge.objects.all().delete()
        Shop.objects.all().delete()

        self.stdout.write('Creating shops...')
        shops = []
        for i in range(1, 11):
            shop = Shop.objects.create(
                name=f"Shop {i}",
                lat=19.19 + (random.random() * 0.05),
                lng=72.97 + (random.random() * 0.05),
                garbage_weight=random.randint(5, 100)
            )
            shops.append(shop)

        self.stdout.write('Creating edges...')
        for i in range(len(shops) - 1):
            Edge.objects.create(
                from_shop=shops[i],
                to_shop=shops[i+1],
                distance_km=round(random.uniform(1.0, 10.0), 2)
            )
            # Add some cross edges
            if i < len(shops) - 2:
                Edge.objects.create(
                    from_shop=shops[i],
                    to_shop=shops[i+2],
                    distance_km=round(random.uniform(2.0, 15.0), 2)
                )

        self.stdout.write(self.style.SUCCESS('Successfully seeded shops and edges!'))
