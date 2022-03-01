from django.db import models
# from allauth.account import app_settings
from allauth.account.signals import user_signed_up
# from allauth.socialaccount.signals import pre_social_login
# from allauth.account.utils import perform_login
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser, UserManager
from django.conf import settings

from rooms.models import Room

class MyUser(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_security = models.BooleanField(default=False)

    objects = UserManager()

    class Meta:
        db_table = 'auth_user'

    def __str__(self):
        return self.username

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="profile", on_delete=models.CASCADE)
    room = models.ForeignKey(Room, null=True, blank=True, related_name="students", on_delete=models.SET_NULL)
    rollno = models.CharField(max_length=10, unique=True)

    def save(self, *args, **kwargs):
        if self.room:
            if self.room.students.count() < self.room.beds:
                super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)
        

    def __str__(self):
        return f"{self.rollno}"

# @receiver(pre_social_login)
# def link_to_local_user(sender, request, sociallogin, **kwargs):
#     email_address = sociallogin.account.extra_data['email']
#     users = MyUser.objects.filter(email=email_address)
#     if users:
#         perform_login(request, users[0], email_verification=app_settings.EMAIL_VERIFICATION)

@receiver(user_signed_up)
def createProfile(sender=MyUser, **kwargs):
    username = kwargs['user'].username
    user = MyUser.objects.get(username = username)
    user.is_student = True
    user.is_security = False
    user.save()
    rollno = user.email.split("@")[0]
    Profile.objects.create(user=user, rollno=rollno)