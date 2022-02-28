from django.contrib import admin
from .models import Hostel, Room
from .forms import HostelAdminForm, RoomAdminForm
from users.models import Profile
# Register your models here.

class HostelAdmin(admin.ModelAdmin):
    form = HostelAdminForm
    search_fields = ['name']

class ProfileInline(admin.StackedInline):
    model = Profile
    readonly_fields = ['rollno']
    verbose_name = "student"
    can_delete = False
    fields = ['rollno']
    
    def get_max_num(self, request, obj=None, **kwargs):
        if obj:
            return obj.beds
        return 1

class RoomAdmin(admin.ModelAdmin):
    form = RoomAdminForm
    inlines = [
        ProfileInline,
    ]
    raw_id_fields = ['hostel']
    list_filter = ['hostel']
    search_fields = ['number']

admin.site.register(Hostel, HostelAdmin)
admin.site.register(Room, RoomAdmin)