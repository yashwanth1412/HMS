# Generated by Django 4.0.2 on 2022-03-01 05:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_profile_rollno'),
        ('rooms', '0007_delete_requestchangeroom'),
    ]

    operations = [
        migrations.CreateModel(
            name='RequestChangeRoom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.TextField()),
                ('remarks', models.TextField(blank=True, null=True)),
                ('preferences', models.ManyToManyField(blank=True, related_name='room_preferences', to='rooms.Room')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requeststo_changeroom', to='users.profile')),
            ],
        ),
    ]
