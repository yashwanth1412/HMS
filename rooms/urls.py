from django.urls import path
from . import views

app_name = "rooms"

urlpatterns = [
    path('request-change-room', views.RequestChangeRoomView.as_view(), name="request-change-room"),
]