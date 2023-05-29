import os

import django
from django.db import models

class Location(models.Model):
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zip = models.CharField(max_length=5)
    lat = models.FloatField()
    lng = models.FloatField()

class Good(models.Model):
    pickup_location = models.ForeignKey(Location, related_name="good_pickup", on_delete=models.CASCADE)
    delivery_location = models.ForeignKey(Location, related_name="good_delivery", on_delete=models.CASCADE)
    weight = models.IntegerField()
    description = models.TextField()

class Car(models.Model):
    number = models.CharField(max_length=255)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    carrying_capacity = models.IntegerField()
