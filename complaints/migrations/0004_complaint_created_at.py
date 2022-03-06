# Generated by Django 3.2.1 on 2022-03-06 05:43

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('complaints', '0003_alter_complaint_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='complaint',
            name='created_at',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
