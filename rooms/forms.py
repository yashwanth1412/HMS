from django import forms
from .models import Room
from django.core.exceptions import ObjectDoesNotExist

class RoomAdminForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = '__all__'

    def clean(self):
        cleaned_data = self.cleaned_data
        no = cleaned_data.get('number')
        beds = cleaned_data.get('beds')

        try:
            room = Room.objects.get(number=no)
        except ObjectDoesNotExist:
            room = None
        
        if room and (room.students.count() > beds):
            raise forms.ValidationError(f"Cannot decrease beds in Room: {no} since all of them are occupied.")
        return cleaned_data