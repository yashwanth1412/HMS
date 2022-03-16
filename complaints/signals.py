from .models import Complaint
from django.db.models.signals import post_save, pre_save
from django.core.mail import send_mail
from django.dispatch import receiver
from users.models import MyUser
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

@receiver(post_save, sender=Complaint)
def create_profile(sender, instance, created, **kwargs):
    if created:
        try:
            send_mail(
                'Complaint successfully registered',
                f"A ticket {instance.pk} has been generated for your complaint:{instance.complaint}",
                None,
                [instance.user.user.email],
                fail_silently=False,
            )

            staff = MyUser.objects.filter(is_superuser=True)
            emails = [i.email for i in staff]

            send_mail(
                'A complaint has been registered',
                f"A complaint has been registered by {instance.user.user.username}, complaint:{instance.complaint}",
                None,
                emails,
                fail_silently=False,
            )
        except:
            print("Error sending mail")

    elif instance.status == "resolved":
        msg = f"Your complaint: {instance.complaint} has been successfully resolved."
        if instance.remarks:
            msg += f"Remarks: {instance.remarks}"
        try:
            send_mail(
                f'Your Complaint#{instance.pk} has been successfully resolved',
                msg,
                None,
                [instance.user.user.email],
                fail_silently=False,
            )
        except:
            print("Error sending mail")
