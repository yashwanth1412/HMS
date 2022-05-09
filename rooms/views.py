from http.client import HTTPResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.exceptions import PermissionDenied
from django.views import View
from django.contrib import messages
from .forms import RequestChangeRoomForm
from .models import Room, Hostel

# Create your views here.
@method_decorator(login_required, name='dispatch')
class RequestChangeRoomView(View):
    form = RequestChangeRoomForm
    reverse_url = "users:profile"

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST)
        if form.is_valid():
            s = form.save(commit=False)
            s.student = request.user.profile
            s.save()
            form.save_m2m()
            messages.success(request, f"Successfully requested to change room")
            return redirect(reverse(self.reverse_url))
        messages.error(request, form.errors)
        return redirect(reverse(self.reverse_url))

@login_required  
def layout(request, hstl_name="Krishna"):
    if not request.user.is_staff:
        raise PermissionDenied()
    try: 
        hstl = Hostel.objects.get(name=hstl_name)
    except:
        return HTTPResponse("No hostel with the name exists")
    f_rooms = Room.objects.filter(hostel=hstl, number__startswith="F").order_by("number")
    rooms = Room.objects.filter(hostel=hstl, number__startswith="G").order_by("number")

    upt_rooms = []
    d = []
    for room in rooms:
        d.append(room.beds - room.students.count())
        upt_rooms.append((room, room.beds - room.students.count()))
    
    d2 = []
    fpt_rooms = []
    for room in f_rooms:
        d2.append(room.beds - room.students.count())
        fpt_rooms.append((room, room.beds - room.students.count()))

    return render(request, "rooms/home.html", {
        "hstl_name" : hstl_name,
        "rooms" : rooms, "d" : d, "upt_rooms" : upt_rooms,
        "f_rooms" : f_rooms, "d2" : d2, "fpt_rooms" : fpt_rooms,
        })
        