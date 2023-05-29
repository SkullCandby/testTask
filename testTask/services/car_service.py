import traceback

from testTask.models import Car, Location
from .location_service import location_service

"""
"""


class car_service:
    def __init__(self):
        self.model = Car
        self.location_service = location_service()

    def edit_car(self, id: int, zip: str):
        try:
            location_id =  self.location_service.get_location_by_zip(zip)["data"]
            self.model.objects.filter(id=id).update(location_id=location_id)
            return {"status": "успех", "message": "Местоположение успешно обновлено"}
        except Exception as e:
            return {"status": "ошибка", "message": "При обновлении местоположения произошла ошибка: " + str(e)}

    def get_all_cars(self):
        try:
            cars = list(self.model.objects.all())
            return {"status": "успех", "data": cars}
        except Exception as e:
            return {"status": "ошибка", "message": "При получении всех машин произошла ошибка: " + str(e)}

    def get_all_cars_by_location(self, location_id):
        try:
            cars = self.get_all_cars()['data']
            lst = [(car.number,  self.location_service.get_destination_by_id(location_id, car.location_id)["data"]) for car in cars]
            return {"status": "успех", "data": lst}
        except Exception as e:
            return {"status": "ошибка", "message": "При получении всех машин по местоположению произошла ошибка: " + str(e)}

    def get_all_cars_distances_by_location(self, location_id, lim=450):
        # Фильтр списка грузов (вес, мили ближайших машин до грузов);
        try:
            cars = self.get_all_cars()['data']
            lst = list(filter(lambda x: x <= lim, [self.location_service.get_destination_by_id(location_id, car.location_id)["data"] for car in cars]))
            return {"status": "успех", "data": len(lst)}
        except Exception as e:
            return {"status": "ошибка", "message": "При получении всех расстояний до машин по местоположению произошла ошибка: " + str(e)}



    def update_location(self):
        # Автоматическое обновление локаций всех машин раз в 3 минуты (локация меняется на другую случайную).
        try:
            cars = Car.objects.all()
            for car in cars:
                location = Location.objects.order_by('?').first()
                with open("readme.txt", "a") as f:
                    f.write(location.state)
                    print(location.state)

                car.location = location
                car.save()
        except Exception as e:
            print("An error occurred: ", str(e))
            print(traceback.format_exc())




