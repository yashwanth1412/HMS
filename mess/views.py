from django.shortcuts import render
from django.http import HttpResponse
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

    for d, food_day in items.items():
        print(d)
        for x,y in food_day.items():
            print(x)
            print(y)
    
    return render(request, "mess/menu.html", {"items" : items})