from django.urls import path
from . import views

# Адрес в браузере определяет, какая функция из views.py будет вызвана.
urlpatterns = [
    path("", views.dogs, name="home"),
    path("dogs/", views.dogs, name="dogs"),
    path("pokemon/", views.team, name="team"),
    path("pokemon/add/", views.add_pokemon, name="add_pokemon"),
    path("pokemon/remove/", views.remove_pokemon, name="remove_pokemon"),
    path("pokemon/battle/", views.battle, name="battle"),
]
