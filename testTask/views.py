from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .services.car_service import car_service
from .services.good_service import good_service
from django_q.tasks import schedule
from datetime import timedelta

car_service_ = car_service()
good_service_ = good_service()
@csrf_exempt
def edit_car(request, id):
    if request.method == 'PUT':
        zip = request.GET.get('zip')
        response = car_service_.edit_car(id, zip)
        return JsonResponse({'message': response})
    else:
        return JsonResponse({'message': 'Неправильный метод запроса'})

def get_all_cars(request):
    if request.method == 'GET':
        cars = car_service_.get_all_cars()["data"]
        car_list = [{'id': car, 'number': car.number} for car in cars]
        return JsonResponse({'cars': car_list})
    else:
        return JsonResponse({'message': 'Неправильный метод запроса'})

def get_all_cars_by_location(request, location_id):
    if request.method == 'GET':
        cars = car_service_.get_all_cars_by_location(location_id)["data"]
        print(cars)
        car_list = [{'number': car[0], 'distance': car[1]} for car in cars]
        return JsonResponse({'cars': car_list})
    else:
        return JsonResponse({'message': 'Неправильный метод запроса'})

def get_all_cars_distances_by_location(request, location_id):
    if request.method == 'GET':
        count = car_service_.get_all_cars_distances_by_location(location_id)
        return JsonResponse({'count': count})
    else:
        return JsonResponse({'message': 'Неправильный метод запроса'})

@csrf_exempt
def create_good(request):
    if request.method == 'POST':
        pick_up_zip = request.GET.get('pick_up')
        delivery_zip = request.GET.get('delivery')
        response = good_service_.create_good(pick_up_zip, delivery_zip)["message"]
        return JsonResponse({'good_id': response})
    else:
        return JsonResponse({'message': 'Неправильный метод запроса'})

def get_goods(request):
    if request.method == 'GET':
        goods = good_service_.get_goods()
        return JsonResponse({'goods': goods})
    else:
        return JsonResponse({'message': 'Неправильный метод запроса'})

def certain_good(request, id):
    if request.method == 'GET':
        good = good_service_.certain_good(id)
        return JsonResponse(good)
    else:
        return JsonResponse({'message': 'Неправильный метод запроса'})

@csrf_exempt
def update_good(request, id):
    if request.method == 'PUT':
        weight = request.GET.get('weight')
        description = request.GET.get('description')
        response = good_service_.update_good(id, weight, description)
        return JsonResponse({'message': response})
    else:
        return JsonResponse({'message': 'Неправильный метод запроса'})

def delete_good(request, id):
    if request.method in ('GET', 'DELETE'):
        # при отправки delete запроса отправлялся get
        response = good_service_.delete_good(id)
        return JsonResponse({'message': response})
    else:
        return JsonResponse({'message': 'Неправильный метод запроса'})
def filter_goods(request):
    if request.method == 'GET':
        weight = float(request.GET.get('weight'))
        dist = float(request.GET.get('dist'))
        response = good_service_.filter_goods(weight, dist)
        return JsonResponse({'message': response})
    else:
        return JsonResponse({'message': 'Неправильный метод запроса'})

# Каждые 3 минуты обновлять локацию
schedule('testTask.listeners.update_car_locations', schedule_type='I', minutes=3)
