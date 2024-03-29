# Generated by Django 4.0.2 on 2022-03-01 12:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0009_requestchangeroom_status'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='requestchangeroom',
            options={'verbose_name': 'Request to change room', 'verbose_name_plural': 'Requests to change room'},
        ),
        migrations.AddField(
            model_name='requestchangeroom',
            name='allocate_room',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='rooms.room'),
        ),
    ]
