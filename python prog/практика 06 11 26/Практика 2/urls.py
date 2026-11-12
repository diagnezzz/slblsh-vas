from django.urls import path

from views import dogs


# При открытии главной страницы запускается функция dogs из views.py.
urlpatterns = [path("", dogs, name="dogs")]
