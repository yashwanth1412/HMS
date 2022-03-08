from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import never_cache
from django.shortcuts import get_object_or_404
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
        form = self.form(request.POST or None, request.FILES or None)
        if form.is_valid():
            s = form.save(commit=False)
            s.user = request.user.profile
            s.save()
            messages.success(request, "Successfully lodged the complaint")
            return redirect(reverse('complaints:view'))
        
        messages.error(request, "Couldn't file complaint.")
        return render(request, self.template_name, {
            "form" : form
        })

@method_decorator(login_required, name='dispatch')
class ViewComplaintsView(View):
    template_name = 'complaints/view_complaints.html'
    
    def get(self, request, *args, **kwargs):
        complaints = Complaint.objects.filter(user=request.user.profile)

        for complaint in complaints:
            if complaint.status == "pending":
                complaint.status = False
            else:
                complaint.status = True

        return render(request, self.template_name, {
            "complaints": complaints
        })

@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required, name='dispatch')
class EditComplaintView(View):
    template_name = "complaints/edit_complaint.html"
    form = ComplaintForm

    def get(self, request, id, *args, **kwargs):
        complaint = get_object_or_404(Complaint, pk=id)
        if complaint.user != request.user.profile:
            messages.error(request, "You are not authorized")
            return redirect(reverse("complaints:view"))
        elif complaint.status == "resolved":
            messages.warning(request, f"Cannot edit Complaint id: {id} since it's already resolved")
            return redirect(reverse("complaints:view"))
        else:
            form = self.form(instance=complaint)
            return render(request, self.template_name, {
                "form" : form,
                "complaint" : complaint
            })
    
    def post(self, request, id, *args, **kwargs):
        complaint = get_object_or_404(Complaint, pk=id)
        if complaint.user != request.user.profile:
            messages.error(request, "You are not authorized")
            return redirect(reverse("complaints:view"))
        elif complaint.status == "resolved":
            messages.warning(request, f"Cannot edit Complaint id: {id} since it's already resolved")
            return redirect(reverse("complaints:view"))
        else:
            form = self.form(request.POST or None, request.FILES or None, instance=complaint)
            if form.is_valid():
                s = form.save(commit=False)
                s.save()
                messages.success(request, f"Successfully edited the complaint id:{id}")
                return redirect(reverse('complaints:view'))
        
        messages.error(request, "Couldn't edit complaint.")
        return render(request, self.template_name, {
            "form" : form
        })

@login_required
def delete_complaint(request, id):
    complaint = get_object_or_404(Complaint, pk=id)
    if complaint.user != request.user.profile:
        messages.error(request, "You are not authorized")
    elif complaint.status == "resolved":
        messages.warning(request, f"Cannot delete Complaint id: {id} since it's already resolved")
    else:
        complaint.delete()
        messages.success(request, f"Successfully deleted Complaint id: {id}")
    return redirect(reverse("complaints:view"))
