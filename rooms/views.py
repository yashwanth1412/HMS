from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib import messages
from .forms import RequestChangeRoomForm

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
        