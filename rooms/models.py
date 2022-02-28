from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.
class Hostel(models.Model):
    name =  models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.name} block"

class Room(models.Model):
    hostel = models.ForeignKey(Hostel, related_name="rooms", on_delete=models.CASCADE)
    number = models.CharField(max_length=5, verbose_name="Room no")
    beds = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])

    class Meta:
        unique_together = ["hostel", "number"]
        ordering = ['hostel', 'number']

    def __str__(self):
        return f"{self.hostel.name} - Room no: {self.number}"