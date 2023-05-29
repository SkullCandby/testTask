from testTask.models import Good
from .car_service import car_service
from .location_service import location_service
import json
from random import randint


class good_service:
    def __init__(self):
        self.model = Good
        self.location_service = location_service()
        self.car_service = car_service()

    def create_good(self, pick_up_zip: str, delivery_zip: str):
        try:
            pick_up_location = self.location_service.get_location_by_zip(zip=pick_up_zip)["data"]
            print(pick_up_location)
            delivery_location = self.location_service.get_location_by_zip(zip=delivery_zip)["data"]

            weight = randint(1, 1000)
            description = f"Груз из {pick_up_zip} в {delivery_zip}"
            new_good = self.model(
                pickup_location_id=pick_up_location.id,
                delivery_location_id=delivery_location.id,
                weight=weight,
                description=description
            )
            new_good.save()
            return {"status": "успех", "message": f"Груз успешно создан с id {new_good.id}"}
        except Exception as e:
            return {"status": "ошибка", "message": f"Ошибка при создании груза: {e}"}

    def get_goods(self, distance=450):
        try:
            goods = self.model.objects.all()
            result = []
            for good in goods:
                pick_up = self.location_service.location_by_id(good.pickup_location_id)["data"]
                delivery = self.location_service.location_by_id(good.delivery_location_id)["data"]
                cars = self.car_service.get_all_cars_distances_by_location(good.pickup_location_id, distance)["data"]
                inner = {
                    "pick_up": f"{pick_up.lat}, {pick_up.lng}",
                    "delivery": f"{delivery.lat}, {delivery.lng}",
                    "cars": cars,
                }
                result.append(inner)
            return {"status": "успех", "message": "Все грузы успешно получены", "data": result}
        except Exception as e:
            return {"status": "ошибка", "message": f"Ошибка при получении грузов: {e}"}

    def certain_good(self, id: int):
        try:
            good = self.model.objects.get(id=id)
            cars = self.car_service.get_all_cars_by_location(good.pickup_location_id)["data"]
            pick_up = self.location_service.location_by_id(good.pickup_location_id)["data"]
            delivery = self.location_service.location_by_id(good.delivery_location_id)["data"]
            data = {
                "pick_up": f"{pick_up.lat}, {pick_up.lng}",
                "delivery": f"{delivery.lat}, {delivery.lng}",
                "weight": f"{good.weight}",
                "description": f"{good.description}",
                "cars": cars,
            }
            return {"status": "успех", "message": f"Информация о грузе с id {id} успешно получена", "data": data}
        except Exception as e:
            return {"status": "ошибка", "message": f"Ошибка при получении информации о грузе: {e}"}

    def update_good(self, id: int, weight: int, description: str):
        try:
            self.model.objects.filter(id=id).update(weight=weight, description=description)
            return {"status": "успех", "message": f"Груз с id {id} успешно обновлён"}
        except Exception as e:
            return {"status": "ошибка", "message": f"Ошибка при обновлении груза: {e.__str__()}"}

    def delete_good(self, id: int):
        try:
            self.model.objects.filter(id=id).delete()
            return {"status": "успех", "message": f"Груз с id {id} успешно удалён"}
        except Exception as e:
            return {"status": "ошибка", "message": f"Ошибка при удалении груза: {e}"}

    def filter_goods(self, weight: int, dist: int):
        try:
            by_weight = self.model.objects.filter(weight__lte=weight)
            filtered_goods = []
            distances = []
            for good in by_weight:
                cars = self.car_service.get_all_cars()["data"]

                distances = list(filter(lambda x: x <= dist, [self.location_service.get_destination_by_id(car.location_id, good.pickup_location_id)["data"] for
                             car in cars]))

                filtered_goods.append(
                    {
                        "good_id": good.id,
                        "n_of_cars": len(distances)
                    }
                )

            return {"status": "успешно", "message": filtered_goods}

        except Exception as e:
            return {"status": "ошибка", "message": f"Ошибка при фильтрации грузов: {e}"}