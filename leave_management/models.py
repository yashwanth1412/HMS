from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from simple_history.models import HistoricalRecords

User = get_user_model()

STATUS = (
    ('pending', 'Pending'),
    ('accepted', 'Accept'),
    ('declined', 'Decline')
)

# Create your models here.
class LeaveApplication(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.TextField()
    from_date = models.DateField()
    to_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS, default="pending")
    remarks = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(default= timezone.now)

    def __str__(self):
        return f"{self.user.username} applied for leave on {self.created_at}"

TYPE = (
    ('in', 'In'),
    ('out', 'Out')
)

PASS_STATUS = (
    ('draft', 'Draft'),
    ('done', 'Done')
)

class StudentStaffInOutRecords(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=TYPE, default="in")
    status = models.CharField(max_length=20, choices=PASS_STATUS, default="draft")
    request = models.OneToOneField(LeaveApplication, null=True, blank=True, on_delete=models.SET_NULL, related_name="in_out_record")
    reason = models.TextField(null=True, blank=True)
    time = models.DateTimeField(default= timezone.now)

    history = HistoricalRecords()

    class Meta:
        verbose_name = "Student Staff InOut Records"
        verbose_name_plural = "Student Staff InOut Records"

    def __str__(self):
        if self.status == "draft":
            return f"{self.user} applied for outpass"
        if self.type == 'in':
            return f"{self.user} came in to the campus at {self.time}"
        else:
            return f"{self.user} went out of the campus at {self.time}"

phone_validator = RegexValidator('^[0-9]{10}$')

class VisitorRecords(models.Model):
    name = models.CharField(max_length=30)
    phone_number = models.CharField(
                        max_length=10,
                        validators=[phone_validator],
                        null=True, blank=True
                    )
    reason = models.TextField(null=True, blank=True)
    check_in = models.DateTimeField(default=timezone.now)
    check_out = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Visitor Records"
        verbose_name_plural = "Visitor Records"    

    def __str__(self):
        return f"{self.name} visited at {self.check_in}"