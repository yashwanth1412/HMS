from django.shortcuts import render
from .models import FoodItem
from django.db.models import Q

import io
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
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


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return

def test_file(request):
    items = {}
    for day in DAYS:
        items[day] = {}
        for ty in TYPES: 
            items[day][ty] = FoodItem.objects.filter(Q(days__contains=day) & Q(type__contains=ty))

    return render_to_pdf('mess/pdf_menu.html', {"items" : items})