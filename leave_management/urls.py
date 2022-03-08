from django.urls import path
from . import views

app_name = "leave"

urlpatterns = [
    path('view', views.LeaveApplicationView.as_view(), name="view"),
    path('request', views.LeaveApplicationRequestView.as_view(), name="request")
]