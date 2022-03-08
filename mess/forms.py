from django import forms
from .models import FoodItem

class FoodItemAdminForm(forms.ModelForm):
    class Meta:
        model = FoodItem
        fields = "__all__"