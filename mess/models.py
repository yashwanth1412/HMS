from django.db import models
from multiselectfield import MultiSelectField
# Create your models here.
TYPES = (
    ("breakfast", 'BreakFast'),
    ("lunch", "Lunch"),
    ("snacks", "Snacks"),
    ("dinner", "Dinner")
)

DAYS = (
    ("SUN", "Sunday"),
    ("MON", "Monday"),
    ("TUE", "Tuesday"),
    ("WED", "Wednesday"),
    ("THU", "Thursday"),
    ("FRI", "Friday"),
    ("SAT", "Saturday")
)

class FoodItem(models.Model):
    type = MultiSelectField(choices=TYPES)
    name = models.CharField(max_length=30, unique=True)
    days = MultiSelectField(choices=DAYS)

    def __str__(self):
        return self.name.capitalize()
