from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from users.models import MyUser

from .models import LeaveApplication, StudentStaffInOutRecords

@receiver(post_save, sender=LeaveApplication)
def send_leave_mail(sender, instance, created, **kwargs):
    if created:
        staff = MyUser.objects.filter(is_superuser=True)
        emails = [i.email for i in staff]
        try:
            send_mail(
                'Leave Application',
                f"{instance.user.username} has applied for leave. Log on to hostel portal for more info.",
                None,
                emails,
                fail_silently=False,
            )
        except:
            print("Error sending email")
    else:
        if instance.status != 'pending' and instance.user.email:
            msg = f"Your leave application from {instance.from_date} to {instance.to_date} has been {instance.status}. "
            if instance.remarks:
                msg += f"Remarks: {instance.remarks}"

            try:
                send_mail(
                    f'Leave Application for {instance.from_date} to {instance.to_date}',
                    msg,
                    None,
                    [instance.user.email],
                    fail_silently=False,
                )
            except:
                print("Error sending email")



@receiver(post_save, sender=StudentStaffInOutRecords)
def changestatus(sender, instance, created, **kwargs):
    # print(instance.history.all().last().history_user)
    # print(instance.history.all().last().history_user.is_staff)
    # if instance.status == "draft" and instance.history.all().last().history_user.is_staff:
    #     instance.status = "done"
    #     instance.save()

    if instance.status == 'done':
        if instance.type == "in":
            instance.user.campus_status="on_campus"
            instance.user.save()

        else:
            instance.user.campus_status="off_campus"
            instance.user.save()
    
    