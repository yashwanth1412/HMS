from django.urls import path
from . import views

app_name = "mess"

urlpatterns = [
    path('menu', views.menu, name="menu"),
    path('test', views.test_file, name="test")
]