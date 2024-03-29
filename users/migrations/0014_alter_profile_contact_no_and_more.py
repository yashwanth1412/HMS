# Generated by Django 4.0.2 on 2022-05-09 01:38

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_alter_profile_rollno'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='contact_no',
            field=models.CharField(blank=True, max_length=10, null=True, validators=[django.core.validators.RegexValidator('^[0-9]{10}$')]),
        ),
        migrations.AlterField(
            model_name='profile',
            name='emergency_contact_name',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='emergency_contact_phone_no',
            field=models.CharField(blank=True, max_length=10, null=True, validators=[django.core.validators.RegexValidator('^[0-9]{10}$')]),
        ),
    ]
