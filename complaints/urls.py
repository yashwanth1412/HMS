from django.urls import path
from . import views

app_name = "complaints"

urlpatterns = [
    path('', views.ComplaintView.as_view(), name="home")
]