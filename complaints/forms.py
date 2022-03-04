from django import forms
from .models import Complaint

class ComplaintAdminForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['user', 'photo', 'complaint', 'status', 'remarks']

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['photo', 'complaint']