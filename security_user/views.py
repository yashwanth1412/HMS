from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
# Create your views here.

@staff_member_required(login_url="users:login")
def view_outpass(request):
    return render(request, "security_user/layout.html")