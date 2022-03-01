from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.contrib import messages
from django.views.decorators.cache import never_cache
from .forms import ProfileForm
from rooms.forms import RequestChangeRoomForm
from rooms.models import RequestChangeRoom

# Create your views here.
@method_decorator(never_cache, name='dispatch')
class LoginView(View):
    template_name = 'users/login.html'
    reverse_url = "users:home"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse(self.reverse_url))

        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Successfully logged in as {username}")
            return redirect(reverse(self.reverse_url))

        messages.error(request, 'Invalid Username or Password')
        return redirect(reverse("users:login"))

@method_decorator(login_required, name='dispatch')
class HomeView(View):
    template_name = 'users/home.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {
            "msg" : f"Hello {request.user.username}"
        })

@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    template_name = 'users/profile.html'
    profileform = ProfileForm
    requestroomform = RequestChangeRoomForm

    def get(self, request, *args, **kwargs):
        profile = request.user.profile

        room = None
        if profile.room:
            room = f"{profile.room.hostel.name} - Room no: {profile.room.number}"
        data = {'room': room, 'rollno': profile.rollno}
        profileform = self.profileform(initial=data)

        requestroomform = self.requestroomform()
        check_request = RequestChangeRoom.objects.filter(student=profile, status="pending")

        if not check_request:
            exists = False
        else:
            exists = True

        return render(request, self.template_name, {
            "profileform" : profileform,
            "changerequest_exists" : exists,
            "requestroomform" : requestroomform
        })

class LogOutView(View):
    redirect_url = "users:login"

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "You are not logged in")
            return redirect(reverse(self.redirect_url))

        logout(request)

        messages.success(request, "Successfully logged out")
        return redirect(reverse(self.redirect_url))