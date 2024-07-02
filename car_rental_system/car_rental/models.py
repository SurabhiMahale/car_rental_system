from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class User(AbstractUser):
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, default='user')
    groups = models.ManyToManyField(
        Group,
        related_name='car_rental_user_set', 
        blank=True,
        help_text=('The groups this user belongs to. A user will get all permissions '
                   'granted to each of their groups.'),
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='car_rental_user_set',  
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='user',
    )

class Car(models.Model):
    category = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    number_plate = models.CharField(max_length=20, unique=True)
    current_city = models.CharField(max_length=50)
    rent_per_hr = models.IntegerField()
    rent_history = models.JSONField(default=list, blank=True)
