# listeners.py
import traceback
from .models import Car, Location


def update_car_locations():
    try:
        cars = Car.objects.all()
        for car in cars:
            location = Location.objects.order_by('?').first()
            car.location = location
            car.save()
    except Exception as e:
        print("An error occurred: ", str(e))
        print(traceback.format_exc())