from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib import messages
from .models import LeaveApplication
from .forms import LeaveApplicationForm

# Create your views here.
@method_decorator(login_required, name='dispatch')
class LeaveApplicationRequestView(View):
    template_name = "leave/request_leave.html"
    form = LeaveApplicationForm

    def get(self, request, *args, **kwargs):
        form = self.form()
        pending = LeaveApplication.objects.filter(user=request.user, status="pending")
        applied = False 

        application = None
        
        if len(pending) > 0:
            applied = True
            application = pending[0]

        return render(request, self.template_name, {
            "applied" : applied,
            "application" : application,
            "form" : form
        })

    def post(self, request, *args, **kwargs): 
        pending = LeaveApplication.objects.filter(user=request.user, status="pending")
        if len(pending) > 0:
            messages.warning(request, 'You have already applied for leave')
            return redirect(reverse("leave:request"))
            
        form = self.form(request.POST)
        
        if form.is_valid():
            s = form.save(commit=False)
            s.user = request.user
            s.save()
            messages.success(request, "Successfully requested for leave")
            return redirect(reverse('leave:request'))
        
        messages.error(request, form.errors)
        return render(request, self.template_name, {
            "form" : form
        })

@method_decorator(login_required, name='dispatch')
class LeaveApplicationView(View):
    template_name = "leave/view_requests.html"
    
    def get(self, request, *args, **kwargs):
        applications = LeaveApplication.objects.filter(user=request.user)

        return render(request, self.template_name, {
            "applications" : applications
        })