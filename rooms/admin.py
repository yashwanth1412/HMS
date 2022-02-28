from django.contrib import admin
from .models import Room
from .forms import RoomAdminForm
from users.models import Profile
# Register your models here.

class ProfileInline(admin.StackedInline):
    model = Profile
    readonly_fields = ['user']
    verbose_name = "student"
    can_delete = False
    
    def get_max_num(self, request, obj=None, **kwargs):
        if obj:
            return obj.beds
        return 1

class RoomAdmin(admin.ModelAdmin):
    form = RoomAdminForm
    inlines = [
        ProfileInline,
    ]

admin.site.register(Room, RoomAdmin)