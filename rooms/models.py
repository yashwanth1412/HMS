from django.db import models
from django.core.validators import MinValueValidator
from django.conf import settings

# Create your models here.
class Hostel(models.Model):
    name =  models.CharField(max_length=20, unique=True)
    warden = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="warden_hostel")
    representative = models.OneToOneField('users.Profile', null=True, blank=True, on_delete=models.SET_NULL, related_name="rep_hostel")

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

STATUS = (
    ('pending', 'Pending'),
    ('resolved', 'Resolved')
)

class RequestChangeRoom(models.Model):
    student = models.ForeignKey('users.Profile', related_name="requeststo_changeroom", on_delete=models.CASCADE)
    preferences = models.ManyToManyField(Room, blank=True, related_name="room_preferences")
    allocate_room = models.ForeignKey(Room, blank=True, null=True, on_delete=models.SET_NULL)
    reason = models.TextField()
    remarks = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS, default="pending")

    class Meta:
        verbose_name = "Request to change room"
        verbose_name_plural = "Requests to change room"

    def __str__(self):
        return f"{self.student.rollno} request to change room"
