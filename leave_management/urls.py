from django.urls import path
from . import views

app_name = "leave"

urlpatterns = [
    path('view', views.LeaveApplicationView.as_view(), name="view"),
    path('request', views.LeaveApplicationRequestView.as_view(), name="request"),
    path('edit/<int:id>', views.EditLeaveView.as_view(), name="edit"),
    path('delete/<int:id>', views.delete_leave_app, name="delete"),
    path('outpass/<int:id>', views.apply_outpass , name="apply_pass"),
    path('download-visitor-records', views.download_visitor_records, name="download-visitor-records"),
    path('download-studentinout-records', views.download_studentinout_records, name="download-studentinout-records"),
]