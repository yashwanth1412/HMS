from django.urls import path
from . import views

app_name = "security"

urlpatterns = [
    path('view', views.view_outpass, name="view"),
    path('inout-records/', views.view_outpass, name="inout-records"),
    path('outpass', views.view_outpass, name="outpass"),
]