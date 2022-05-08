from django.contrib import admin
from django.utils.html import format_html
from .models import LeaveApplication, StudentStaffInOutRecords, VisitorRecords
from .forms import LeaveApplicationAdminForm, StudentStaffInOutRecordsAdminForm, VisitorRecordsAdminForm
# Register your models here. 

class LeaveApplicationAdmin(admin.ModelAdmin):
    form = LeaveApplicationAdminForm
    list_filter = ['status']
    list_display = ['leave_id', 'user']
    autocomplete_fields = ['user']

    def leave_id(self, obj):
        if obj.status != 'pending':
            color_code = '79b340'
        else:
            color_code = 'd9534c'
        html = '<span style="color: #{};">{}</span>'.format(color_code, f"Leave #id: {obj.id}")
        return format_html(html)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['user', 'reason', 'from_date', 'to_date', 'contact_no', 'destination', 'created_at']
        else:
            return []
    
    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser
    
    class Media:
        js = ('js/alert.js',)

class StudentStaffInOutRecordsAdmin(admin.ModelAdmin):
    form = StudentStaffInOutRecordsAdminForm
    list_filter = ['type', 'status']
    raw_id_fields = ['request']
    autocomplete_fields = ['user']

    change_list_template = 'admin/studentstaffinoutrecords/studentstaffinoutrecords_change_list.html'

    def get_readonly_fields(self, request, obj=None):
        if obj:
            if obj.status == "draft":
                return ['user', 'type', 'request']
            return ['user', 'type', 'request', 'time']
        else:
            return []

    class Media:
        js = ('js/alert.js',)

class VisitorListFilter(admin.SimpleListFilter):
    title = 'Vacancy'
    parameter_name = 'beds'

    def lookups(self, request, model_admin):
        return (
            ('in', 'On campus'),
            ('out', 'Left the campus')
        )

    def queryset(self, request, queryset):
        if not self.value():
            return queryset
        if self.value().lower() == 'in':
            return VisitorRecords.objects.filter(check_out__isnull=True)
        else:
            return VisitorRecords.objects.exclude(check_out__isnull=True)

class VisitorRecordsAdmin(admin.ModelAdmin):
    form = VisitorRecordsAdminForm
    list_filter = [VisitorListFilter]
    change_list_template = 'admin/visitorrecords/visitorrecords_change_list.html'


    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['name', 'reason', 'phone_number', 'check_in']
        else:
            return []
    
    class Media:
        js = ('js/alert.js',)

admin.site.register(LeaveApplication, LeaveApplicationAdmin)
admin.site.register(StudentStaffInOutRecords, StudentStaffInOutRecordsAdmin)
admin.site.register(VisitorRecords, VisitorRecordsAdmin)