# Generated by Django 5.2.3 on 2025-06-29 22:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ambulance', '0002_alter_ambulance_driver'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='individualprofile',
            name='user',
        ),
        migrations.RemoveField(
            model_name='orgadminprofile',
            name='organization',
        ),
        migrations.RemoveField(
            model_name='orgadminprofile',
            name='user',
        ),
        migrations.AddField(
            model_name='customuser',
            name='organization',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='users.organization'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='DriverProfile',
        ),
        migrations.DeleteModel(
            name='IndividualProfile',
        ),
        migrations.DeleteModel(
            name='OrgAdminProfile',
        ),
    ]
