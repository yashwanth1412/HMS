from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import MyUser, Profile, UserRoles
from .forms import MyUserCreationForm, ProfileAdminForm
# register your models

admin.site.site_header = "Hostel Administration" 
admin.site.index_title = "Admin"
admin.site.site_title = "Hostel Administation"

class MyUserAdmin(UserAdmin):
    model = MyUser
    add_form = MyUserCreationForm
    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'User Type',
            {
                'fields': (
                    'is_student',
                    'is_security',
                    'campus_status',
                    'my_role'
                )
            }
        )
    )

    list_display = ['username', 'email']
    list_filter = ['is_student', 'is_security', 'campus_status']
    search_fields = ['username']

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

class ProfileAdmin(admin.ModelAdmin):
    form = ProfileAdminForm
    fields = ['user', 'room', 'rollno', 'gender', 'contact_no', 'address', 'emergency_contact_name', 'emergency_contact_phone_no']
    search_fields = ['rollno']
    autocomplete_fields = ('room',)
    list_filter = ['room__hostel']

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['user']
        else:
            return []

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

admin.site.register(MyUser, MyUserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(UserRoles)
