from django.contrib import admin
from django.utils.html import format_html
from .models import Complaint
from .forms import ComplaintAdminForm
# Register your models here.

class ComplaintAdmin(admin.ModelAdmin):
    form = ComplaintAdminForm
    list_filter = ['status']
    list_display = ['complaint_id', 'user']
    autocomplete_fields = ['user']

    def complaint_id(self, obj):
        if obj.status == 'resolved':
            color_code = '79b340'
        else:
            color_code = 'd9534c'
        html = '<span style="color: #{};">{}</span>'.format(color_code, f"Complaint #id: {obj.id}")
        return format_html(html)


    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['user', 'photo', 'complaint', 'status']
        else:
            return []

    def response_change(self, request, obj):
        obj.status = 'resolved'
        obj.save()
        return super().response_change(request, obj)

admin.site.register(Complaint, ComplaintAdmin)