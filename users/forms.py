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

class ProfileForm(forms.ModelForm):
    username = forms.CharField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    room = forms.CharField()

    class Meta:
        model = Profile
        fields = []
    
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        profile = kwargs.get('instance')
        self.fields['username'].initial = profile.user.username
        self.fields['first_name'].initial = profile.user.first_name
        self.fields['last_name'].initial = profile.user.last_name
        self.fields['email'].initial = profile.user.email
        self.fields['room'].initial = profile.room.number