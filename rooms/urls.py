from django.urls import path
from . import views

app_name = "rooms"

urlpatterns = [
    path('request-change-room', views.RequestChangeRoomView.as_view(), name="request-change-room"),
    path('layout', views.layout, name="layout"),
    path('layout/<str:hstl_name>', views.layout, name="layout"),
]