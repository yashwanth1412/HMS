# Generated by Django 4.0.2 on 2022-05-08 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_profile_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='rollno',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]
