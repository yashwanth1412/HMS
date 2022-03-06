from .models import Complaint
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

@receiver(pre_save, sender=Complaint)
def delete_before_change(sender, instance, **kwargs):
    try: 
        complaint = Complaint.objects.get(pk = instance.pk)
    except Complaint.DoesNotExist:
        complaint = None

    if complaint:
        old_pic = complaint.photo
        new_pic = instance.photo
        
        if old_pic and new_pic:
            if old_pic.url != new_pic.url:
                old_pic.delete(save=False)