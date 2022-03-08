from django.contrib import admin
from .models import FoodItem
from .forms import FoodItemAdminForm 
# Register your models here.

class FoodItemAdmin(admin.ModelAdmin):
    form = FoodItemAdminForm

admin.site.register(FoodItem, FoodItemAdmin)