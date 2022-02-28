from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import MyUser, Profile
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
                    'is_security'
                )
            }
        )
    )

    list_display = ['username', 'email']
    list_filter = ['is_student', 'is_security']
    search_fields = ['username']

class ProfileAdmin(admin.ModelAdmin):
    form = ProfileAdminForm
    readonly_fields = ['user']
    raw_id_fields = ['room']

    fields = ['user', 'room', 'rollno']
    search_fields = ['rollno']

admin.site.register(MyUser, MyUserAdmin)
admin.site.register(Profile, ProfileAdmin)

