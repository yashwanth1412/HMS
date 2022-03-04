from django.urls import path
from . import views

app_name = "complaints"

urlpatterns = [
    path('add', views.ComplaintView.as_view(), name="add-complaint")
]