from django.shortcuts import render
#from easy_pdf.rendering import render_to_pdf_response
from .models import FoodItem
from django.db.models import Q
# Create your views here.

DAYS = ["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"]
TYPES = ["breakfast", "lunch", "snacks", "dinner"]

def menu(request):
    items = {}
    for day in DAYS:
        items[day] = {}
        for ty in TYPES: 
            items[day][ty] = FoodItem.objects.filter(Q(days__contains=day) & Q(type__contains=ty))

    return render(request, "mess/menu.html", {"items" : items})

def test_file(request):
    pass
#     items = {}
#     for day in DAYS:
#         items[day] = {}
#         for ty in TYPES: 
#             items[day][ty] = FoodItem.objects.filter(Q(days__contains=day) & Q(type__contains=ty))

#     return render_to_pdf_response(request, 'mess/pdf_menu.html', {"items" : items})