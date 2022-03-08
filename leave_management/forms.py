from time import timezone
from django import forms
import datetime
from .models import LeaveApplication, StudentStaffInOutRecords, VisitorRecords

class LeaveApplicationAdminForm(forms.ModelForm):
    class Meta:
        model = LeaveApplication
        exclude = ('',)

    def clean_from_date(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("from_date")
        if start_date < datetime.date.today():
            raise forms.ValidationError("Start date should be greater than or equal to today.")
    
    def clean_to_date(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("from_date")
        end_date = cleaned_data.get("to_date")
        if end_date < start_date:
            raise forms.ValidationError("End date should be greater than start date.")

class LeaveApplicationForm(forms.ModelForm):
    from_date = forms.DateField(widget=forms.DateInput(attrs={'class': "form-control", 'type': 'date'}))
    to_date = forms.DateField(widget=forms.DateInput(attrs={'class': "form-control", 'type': 'date'}))

    class Meta:
        model = LeaveApplication
        fields = ['from_date', 'to_date', 'reason']

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("from_date")
        if start_date < datetime.date.today():
            raise forms.ValidationError("Start date should be greater than or equal to today.")
        end_date = cleaned_data.get("to_date")
        if end_date < start_date:
            raise forms.ValidationError("End date should be greater than start date.")

class StudentStaffInOutRecordsAdminForm(forms.ModelForm):
    class Meta:
        model = StudentStaffInOutRecords
        exclude = ('',)
    
    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('type') == 'out':
            request = cleaned_data.get('request')
            if not request:
                raise forms.ValidationError("Valid request is required for going out.")
            elif cleaned_data.get('user') != request.user:
                raise forms.ValidationError("Invalid request.")
            elif request.status != "accepted" :
                raise forms.ValidationError("Not allowed since request is not accepted")
            elif not (request.from_date <= cleaned_data.get('time').date() and cleaned_data.get('time').date() <= request.to_date):
                raise forms.ValidationError(f"Request is not valid for {cleaned_data.get('time')}")

class VisitorRecordsAdminForm(forms.ModelForm):
    class Meta:
        model = VisitorRecords
        exclude = ('',)

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('check_in') and cleaned_data.get('check_out'):
            if cleaned_data.get('check_out') < cleaned_data.get('check_in'):
                raise forms.ValidationError("Check in time cannot be less than check out time")