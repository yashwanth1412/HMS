from django import forms
from .models import Hostel, Room
from django.core.exceptions import ObjectDoesNotExist

ROOM_CHOICES = (
    ('create', 'Create rooms'),
    ('update', 'Update rooms'),
    ('delete', 'Delete rooms')
)

class HostelAdminForm(forms.ModelForm):
    room_options = forms.ChoiceField(choices=ROOM_CHOICES, initial='create')
    start_room = forms.CharField(required=False)
    end_room = forms.CharField(required=False)
    beds = forms.IntegerField(min_value=0, initial=0)

    class Meta:
        model = Hostel
        fields = ['name', 'room_options', 'start_room', 'end_room']

    def clean(self):
        print(self.cleaned_data)
    
        if self.cleaned_data.get('start_room') and self.cleaned_data.get('end_room'):
            if self.cleaned_data.get('start_room')[0] != self.cleaned_data.get('end_room')[0]:
                raise forms.ValidationError(f"Floor numbers of both start and end rooms must be same")
            else:
                hstl_name = self.cleaned_data.get('name')
                hostel = Hostel.objects.get(name=hstl_name)

                start = int(self.cleaned_data.get('start_room')[1:])
                end = int(self.cleaned_data.get('end_room')[1:])
                beds = self.cleaned_data.get('beds')
                floor = self.cleaned_data.get('start_room')[0]
                
                for i in range(start,end+1):
                    number = floor + str(i)
                    try:
                        if self.cleaned_data.get('room_options') == ROOM_CHOICES[0][0]:
                            Room.objects.create(hostel=hostel, number=number, beds=beds)
                        else:
                            room = Room.objects.get(hostel=hostel, number=number)

                            if self.cleaned_data.get('room_options') == ROOM_CHOICES[1][0]:
                                room.beds = beds
                                room.save()
                            else:
                                room.delete()

                    except:
                        if self.cleaned_data.get('room_options') == ROOM_CHOICES[0][0]:
                            raise forms.ValidationError(f"Room already exists")
                        elif self.cleaned_data.get('room_options') == ROOM_CHOICES[1][0]:
                            raise forms.ValidationError(f"Room doesnot exists or has no vacancy")
                        else:
                            raise forms.ValidationError(f"Room doesnot exists")

        return self.cleaned_data

class RoomAdminForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = '__all__'

    def clean(self):
        cleaned_data = self.cleaned_data
        hostel = cleaned_data.get('hostel')
        no = cleaned_data.get('number')
        beds = cleaned_data.get('beds')

        try:
            room = Room.objects.get(hostel=hostel,number=no)
        except ObjectDoesNotExist:
            room = None
        
        if room and (room.students.count() > beds):
            raise forms.ValidationError(f"Cannot decrease beds in Room: {no} since all of them are occupied.")
        return cleaned_data