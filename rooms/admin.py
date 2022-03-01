from django.contrib import admin
from .models import Hostel, Room, RequestChangeRoom
from .forms import HostelAdminForm, RoomAdminForm, RequestChangeRoomAdminForm
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

def get_vacant_rooms():
    room_ids = [room.id for room in Room.objects.all() if room.beds > room.students.count()]
    return Room.objects.filter(id__in = room_ids)

def get_full_rooms():
    room_ids = [room.id for room in Room.objects.all() if room.beds > room.students.count()]
    return Room.objects.exclude(id__in = room_ids)

class RoomListFilter(admin.SimpleListFilter):
    title = 'Vacancy'
    parameter_name = 'beds'

    def lookups(self, request, model_admin):
        return (
            ('available', 'Available'),
            ('non-available', 'Not Available')
        )

    def queryset(self, request, queryset):
        if not self.value():
            return queryset
        if self.value().lower() == 'available':
            return get_vacant_rooms()
        else:
            return get_full_rooms()


class RoomAdmin(admin.ModelAdmin):
    form = RoomAdminForm
    inlines = [
        ProfileInline,
    ]
    autocomplete_fields = ['hostel']
    list_filter = ['hostel', RoomListFilter]
    search_fields = ['number']
    list_per_page = 10

class RequestChangeRoomAdmin(admin.ModelAdmin):
    form = RequestChangeRoomAdminForm
    list_filter = ['status']
    raw_id_fields = ['allocate_room']

    def get_readonly_fields(self, request, obj=None):
        return ['student', 'reason', 'preferences', 'status']
    
    def get_form(self, request, obj=None, **kwargs):
        form = super(RequestChangeRoomAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['allocate_room'].queryset = get_vacant_rooms()
        return form

    def has_add_permission(self, request, obj=None):
        return False
    
    # def has_delete_permission(self, request, obj=None):
    #     return False

    def response_change(self, request, obj):
        if obj.allocate_room:
            profile = obj.student
            profile.room = obj.allocate_room
            profile.save()
        obj.status = 'resolved'
        obj.save()
        return super().response_change(request, obj)

admin.site.register(Hostel, HostelAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(RequestChangeRoom, RequestChangeRoomAdmin)