from django.db import models
from django.utils import timezone
from users.models import Profile

STATUS = (
    ('pending', 'Pending'),
    ('resolved', 'Resolved')
)

# Create your models here.
class Complaint(models.Model):
    user = models.ForeignKey(Profile, related_name="complaints", on_delete=models.CASCADE)
    photo = models.ImageField(upload_to="complaint_pics/", null=True, blank=True)
    complaint = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS, default="pending")
    remarks = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(default= timezone.now)

    class Meta:
        verbose_name = "Complaint"
        verbose_name_plural = "Complaints"
        ordering = ['status', '-created_at']

    def __str__(self):
        return f"Complaint #id: {self.id}"