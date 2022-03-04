from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib import messages
from .models import Complaint
from .forms import ComplaintForm
# Create your views here.
@method_decorator(login_required, name='dispatch')
class ComplaintView(View):
    template_name = "complaints/add_complaint.html"
    form = ComplaintForm
    
    def get(self, request, *args, **kwargs):
        form = self.form()
        return render(request, self.template_name, {
            "form" : form
        })
    
    def post(self, request, *args, **kwargs):
        print(request.POST)
        form = self.form(request.POST or None, request.FILES or None)
        if form.is_valid():
            s = form.save(commit=False)
            s.user = request.user.profile
            s.save()
            messages.success(request, "Sucessfully lodged the complaint")
            return redirect(reverse('complaints:add-complaint'))
        
        messages.error(request, "Couldn't file complaint.")
        return render(request, self.template_name, {
            "form" : form
        })
