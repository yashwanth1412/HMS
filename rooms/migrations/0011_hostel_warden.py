# Generated by Django 4.0.2 on 2022-04-26 19:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rooms', '0010_alter_requestchangeroom_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='hostel',
            name='warden',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='warden_hostel', to=settings.AUTH_USER_MODEL),
        ),
    ]