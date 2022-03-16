from django.urls import path
from . import views

app_name = "complaints"

urlpatterns = [
    path('add', views.ComplaintView.as_view(), name="add-complaint"),
    path('view', views.ViewComplaintsView.as_view(), name="view"),
    path('edit/<int:id>', views.EditComplaintView.as_view(), name="edit"),
    path('delete/<int:id>', views.delete_complaint, name="delete"),
]