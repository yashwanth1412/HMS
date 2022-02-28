from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path('', views.HomeView.as_view(), name="home"),
    path('login', views.LoginView.as_view(), name="login"),
    #path('profile', views.ProfileView.as_view(), name="profile"),
    path('logout', views.LogOutView.as_view(), name="logout"),
]