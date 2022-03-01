from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib import messages

# Create your views here.
@method_decorator(login_required, name='dispatch')
class ComplaintView(View):
    pass