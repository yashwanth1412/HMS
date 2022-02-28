from django.db import models
from allauth.account.signals import user_signed_up
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

    def save(self, *args, **kwargs):
        if self.room:
            room = Room.objects.get(number=self.room.number)
            if room.students.count() < self.room.beds:
                super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)
        

    def __str__(self):
        return f"{self.user.username}'s profile"

@receiver(user_signed_up)
def createProfile(sender=MyUser, **kwargs):
    username = kwargs['user'].username
    user = MyUser.objects.get(username = username)
    user.is_student = True
    user.is_security = False
    user.save()
    Profile.objects.create(user=user)