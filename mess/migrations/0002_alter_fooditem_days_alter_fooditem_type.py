# Generated by Django 4.0.2 on 2022-03-08 21:10

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('mess', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fooditem',
            name='days',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('SUN', 'Sunday'), ('MON', 'Monday'), ('TUE', 'Tuesday'), ('WED', 'Wednesday'), ('THU', 'Thursday'), ('FRI', 'Friday'), ('SAT', 'Saturday')], max_length=27),
        ),
        migrations.AlterField(
            model_name='fooditem',
            name='type',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('breakfast', 'BreakFast'), ('lunch', 'Lunch'), ('snacks', 'Snacks'), ('dinner', 'Dinner')], max_length=29),
        ),
    ]