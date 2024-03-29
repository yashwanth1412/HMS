# Generated by Django 4.0.2 on 2022-03-01 05:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rooms', '0003_alter_room_unique_together'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='room',
            options={'ordering': ['hostel', 'number']},
        ),
        migrations.CreateModel(
            name='RequestChangeRoom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.TextField()),
                ('remarks', models.TextField(blank=True, null=True)),
                ('hostel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requeststo_changeroom', to=settings.AUTH_USER_MODEL)),
                ('room_preferences', models.ManyToManyField(blank=True, null=True, related_name='room_preferences', to='rooms.Room')),
            ],
        ),
    ]
