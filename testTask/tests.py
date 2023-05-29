from django.test import TestCase
from testTask.models import Good, Location, Car
from testTask.services.car_service import car_service
from testTask.services.good_service import good_service
from testTask.services.location_service import location_service


class GoodServiceTestCase(TestCase):

    def setUp(self):
        self.good_service = good_service()
        self.location_1 = Location.objects.create(city='City1', state='State1', zip='12345', lat=1.23, lng=4.56)
        self.location_2 = Location.objects.create(city='City2', state='State2', zip='67890', lat=7.89, lng=0.12)

        self.car1 = Car.objects.create(number="Car1", location=self.location_1, carrying_capacity=100)
        self.car2 = Car.objects.create(number="Car2", location=self.location_2, carrying_capacity=100)
    def test_create_good(self):
        response = self.good_service.create_good(pick_up_zip='12345', delivery_zip='67890')
        self.assertEqual(response['status'], 'успех')
        good_id = int(response['message'].split()[-1])
        good = Good.objects.get(id=good_id)

        self.assertEqual(good.pickup_location_id, self.location_1.id)
        self.assertEqual(good.delivery_location_id, self.location_2.id)
        self.assertIsNotNone(good.weight)
        self.assertIsNotNone(good.description)

    def test_get_goods(self):
        self.good_service.create_good(pick_up_zip='12345', delivery_zip='67890')
        response = self.good_service.get_goods()

        self.assertEqual(response['status'], 'успех')
        self.assertEqual(len(response['data']), 1)

    def test_certain_good(self):

        response_creation = self.good_service.create_good(pick_up_zip='12345', delivery_zip='67890')
        good_id = int(response_creation['message'].split()[-1])
        response = self.good_service.certain_good(id=good_id)

        self.assertEqual(response['status'], 'успех')
        self.assertEqual(int(response['data']['weight']), Good.objects.get(id=good_id).weight)
        self.assertEqual(response['data']['description'], Good.objects.get(id=good_id).description)

    def test_update_good(self):
        response_creation = self.good_service.create_good(pick_up_zip='12345', delivery_zip='67890')
        good_id = int(response_creation['message'].split()[-1])
        response = self.good_service.update_good(id=good_id, weight=200, description='New description')
        self.assertEqual(response['status'], 'успех')
        good = Good.objects.get(id=good_id)
        self.assertEqual(good.weight, 200)
        self.assertEqual(good.description, 'New description')

    def test_delete_good(self):
        response_creation = self.good_service.create_good(pick_up_zip='12345', delivery_zip='67890')
        good_id = int(response_creation['message'].split()[-1])
        response = self.good_service.delete_good(id=good_id)

        self.assertEqual(response['status'], 'успех')
        with self.assertRaises(Good.DoesNotExist):
            Good.objects.get(id=good_id)

    def test_filter_goods(self):
        self.good_service.create_good(pick_up_zip='12345', delivery_zip='67890')
        response = self.good_service.filter_goods(weight=131313131, dist=1241414141441)

        self.assertEqual(response['status'], 'успешно')
        self.assertEqual(len(response['message']), 1)

class CarServiceTestCase(TestCase):
    def setUp(self):
        self.car_service = car_service()
        location_1 = Location.objects.create(city="TestCity1", state="TestState1", zip="00000", lat=0.0, lng=0.0)
        location_2 = Location.objects.create(city="TestCity2", state="TestState2", zip="11111", lat=1.0, lng=1.0)

        Car.objects.create(number="Car1", location=location_1, carrying_capacity=100)
        Car.objects.create(number="Car2", location=location_2, carrying_capacity=100)

    def test_edit_car(self):
        car_id = Car.objects.get(number="Car1").id
        response = self.car_service.edit_car(car_id, "11111")

        self.assertEqual(response['status'], 'успех')
        self.assertEqual(response['message'], 'Местоположение успешно обновлено')
        self.assertEqual(Car.objects.get(id=car_id).location.zip, "11111")

    def test_get_all_cars(self):
        response = self.car_service.get_all_cars()
        self.assertEqual(response['status'], 'успех')
        self.assertEqual(len(response['data']), 2)

    def test_get_all_cars_by_location(self):
        location_id = Location.objects.get(zip="00000").id
        response = self.car_service.get_all_cars_by_location(location_id)

        self.assertEqual(response['status'], 'успех')
        self.assertEqual(len(response['data']), 2)

    def test_get_all_cars_distances_by_location(self):
        location_id = Location.objects.get(zip="00000").id
        response = self.car_service.get_all_cars_distances_by_location(location_id)

        self.assertEqual(response['status'], 'успех')
        self.assertEqual(response['data'], 2)


class LocationServiceTestCase(TestCase):
    def setUp(self):
        self.location_service = location_service()

        Location.objects.create(city="TestCity1", state="TestState1", zip="00000", lat=0.0, lng=0.0)
        Location.objects.create(city="TestCity2", state="TestState2", zip="11111", lat=1.0, lng=1.0)

    def test_get_location_by_zip(self):
        response = self.location_service.get_location_by_zip("00000")

        self.assertEqual(response['status'], 'успех')
        self.assertEqual(response['data'].zip, "00000")

    def test_location_by_id(self):
        location_id = Location.objects.get(zip="00000").id
        response = self.location_service.location_by_id(location_id)

        self.assertEqual(response['status'], 'успех')
        self.assertEqual(response['data'].id, location_id)

    def test_get_destination_by_id(self):
        location_id_1 = Location.objects.get(zip="00000").id
        location_id_2 = Location.objects.get(zip="11111").id
        response = self.location_service.get_destination_by_id(location_id_1, location_id_2)

        self.assertEqual(response['status'], 'успех')
        self.assertIsNotNone(response['data'])
