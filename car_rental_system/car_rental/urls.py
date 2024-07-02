from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('car/create/', views.create_car, name='create_car'),
    path('car/get-rides/', views.get_rides, name='get_rides'),
    path('car/rent/', views.rent_car, name='rent_car'),
    path('car/update-rent-history/', views.update_rent_history, name='update_rent_history'),
]
