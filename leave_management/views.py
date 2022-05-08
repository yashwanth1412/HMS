from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.shortcuts import get_object_or_404
from django.views import View
from django.contrib import messages
from .models import LeaveApplication, StudentStaffInOutRecords
from .forms import LeaveApplicationForm
from datetime import datetime

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

        print(form.errors)
        
        messages.error(request, form.errors)
        return render(request, self.template_name, {
            "form" : form
        })

@method_decorator(login_required, name='dispatch')
class LeaveApplicationView(View):
    template_name = "leave/view_requests.html"
    
    def get(self, request, *args, **kwargs):
        applications = LeaveApplication.objects.filter(user=request.user).order_by('-created_at', '-status')

        for application in applications:
            application.outpass_valid = False
            if (datetime.now().date() <= application.to_date):
                application.outpass_valid = True

        return render(request, self.template_name, {
            "applications" : applications
        })

@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required, name='dispatch')
class EditLeaveView(View):
    template_name = "leave/edit_leave.html"
    form = LeaveApplicationForm

    def get(self, request, id, *args, **kwargs):
        leave_app = get_object_or_404(LeaveApplication, pk=id)
        if leave_app.user != request.user:
            messages.error(request, "You are not authorized")
            return redirect(reverse("leave:view"))
        elif leave_app.status != "pending":
            messages.warning(request, f"Cannot edit Leave Application id: {id} since it's already {leave_app.status}")
            return redirect(reverse("leave:view"))
        else:
            form = self.form(instance=leave_app)
            return render(request, self.template_name, {
                "form" : form,
                "leave_app" : leave_app
            })
    
    def post(self, request, id, *args, **kwargs):
        leave_app = get_object_or_404(LeaveApplication, pk=id)
        if leave_app.user != request.user:
            messages.error(request, "You are not authorized")
            return redirect(reverse("leave:view"))
        elif leave_app.status != "pending":
            messages.warning(request, f"Cannot edit Leave Application id: {id} since it's already {leave_app.status}")
            return redirect(reverse("leave:view"))
        else:
            form = self.form(request.POST or None, request.FILES or None, instance=leave_app)
            if form.is_valid():
                s = form.save(commit=False)
                s.save()
                messages.success(request, f"Successfully edited the Leave Application id: {id}")
                return redirect(reverse('leave:view'))
        
        messages.error(request, "Couldn't edit application.")
        return render(request, self.template_name, {
            "form" : form
        })

@login_required
def delete_leave_app(request, id):
    leave_app = get_object_or_404(LeaveApplication, pk=id)
    if leave_app.user != request.user:
        messages.error(request, "You are not authorized")
    elif leave_app.status != "pending":
        messages.warning(request, f"Cannot delete Leave Application id: {id} since it's already {leave_app.status}")
    else:
        leave_app.delete()
        messages.success(request, f"Successfully deleted Leave Application id: {id}")
    return redirect(reverse("leave:view"))

@login_required
def apply_outpass(request, id):
    leave_app = get_object_or_404(LeaveApplication, pk=id)
    if leave_app.user != request.user:
        messages.error(request, "You are not authorized")
    elif leave_app.status != "accepted":
        messages.warning(request, f"Cannot apply for out pass")
    elif not (datetime.now().date() <= leave_app.to_date):
        messages.error(request, "Request is not valid")
    else:
        outpass = StudentStaffInOutRecords(user=request.user, request=leave_app, type="out")
        outpass.save()
        messages.success(request, "Successfully applied outpass")
    
    return redirect(reverse("leave:view"))