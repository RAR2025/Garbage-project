from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.
class Shop(models.Model):
    name = models.CharField(max_length=255)
    lat = models.FloatField()
    lng = models.FloatField()
    garbage_weight = models.FloatField(default= 0.0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name



class Edge(models.Model):
    from_shop = models.ForeignKey(
        Shop,
        on_delete=models.CASCADE,
        related_name="outgoing_edge",
    )
    to_shop = models.ForeignKey(
        Shop,
        on_delete=models.CASCADE,
        related_name="incomming_edge",
    )
    distance_km = models.FloatField()

    def __str__(self) :
        return f"{self.from_shop} -> {self.to_shop} ({self.distance_km} km)"

    def clean(self):
        if self.to_shop == self.from_shop:
            raise ValidationError(
                "source and Destination shops cannot be same"
            )