from django.contrib import admin
from django.urls import path

from .views import (
    edit_car, get_all_cars, get_all_cars_by_location, get_all_cars_distances_by_location,
    create_good, get_goods, certain_good, update_good, delete_good, filter_goods
)

urlpatterns = [
    path('car/edit/<int:id>/', edit_car, name='edit_car'),
    path('car/all/', get_all_cars, name='get_all_cars'),
    path('car/all/filter/', filter_goods),
    path('car/location/<int:location_id>/', get_all_cars_by_location, name='get_all_cars_by_location'),
    path('car/distance/<int:location_id>/', get_all_cars_distances_by_location, name='get_all_cars_distances_by_location'),

    path('good/create/', create_good, name='create_good'),
    path('good/all/', get_goods, name='get_goods'),
    path('good/<int:id>/', certain_good, name='certain_good'),
    path('good/update/<int:id>/', update_good, name='update_good'),
    path('good/delete/<int:id>/', delete_good, name='delete_good'),

    path('admin/', admin.site.urls),
]