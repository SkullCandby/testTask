from django.core.exceptions import ObjectDoesNotExist

from ..models import Location
from geopy.distance import geodesic
class location_service:
    def __init__(self):
        pass

    def get_location_by_zip(self, zip: str):
        try:
            location = Location.objects.get(zip=zip)
            return {"status": "успех", "data": location}
        except ObjectDoesNotExist:
            return {"status": "ошибка", "message": "Местоположение с данным zip-кодом не найдено"}

    def location_by_id(self, id: int):
        try:
            location = Location.objects.get(id=id)
            return {"status": "успех", "data": location}
        except ObjectDoesNotExist:
            return {"status": "ошибка", "message": "Местоположение с данным id не найдено"}

    def get_destination_by_id(self, id_from: int, id_to: int):
        try:
            loc_from = Location.objects.get(id=id_from)
            loc_to = Location.objects.get(id=id_to)
            from_ = (loc_from.lat, loc_from.lng)
            to_ = (loc_to.lat, loc_to.lng)
            distance = geodesic(from_, to_).miles
            return {"status": "успех", "data": distance}
        except ObjectDoesNotExist:
            return {"status": "ошибка", "message": "Местоположение с данным id не найдено"}