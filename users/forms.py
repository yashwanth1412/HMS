from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import MyUser, Profile


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = MyUser
        fields = '__all__'

class ProfileAdminForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'

    def clean(self):
        cleaned_data = self.cleaned_data
        room = cleaned_data.get('room')
        if room and (room.students.count() >= room.beds):
            raise forms.ValidationError(f"There is no vacancy in the Room: {room.number}. Select another room.")
        return cleaned_data

class ProfileForm(forms.Form):
    room = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control", 'required' : False}))
    rollno = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control"}))

class ProfileEditForm(forms.ModelForm):
    contact_no = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control"}))
    emergency_contact_name = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control"}))
    emergency_contact_phone_no = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control"}))

    class Meta:
        model = Profile
        fields = ['contact_no', 'address', 'gender', 'emergency_contact_name', 'emergency_contact_phone_no']