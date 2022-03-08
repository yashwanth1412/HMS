from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import StudentStaffInOutRecords

@receiver(post_save, sender=StudentStaffInOutRecords)
def changestatus(sender, instance, created, **kwargs):
    if instance.type == "in":
        instance.user.campus_status="on_campus"
        instance.user.save()

    else:
        instance.user.campus_status="off_campus"
        instance.user.save()
    