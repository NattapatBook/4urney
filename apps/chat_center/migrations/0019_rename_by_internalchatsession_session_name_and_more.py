# Generated by Django 5.1.3 on 2025-01-22 03:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat_center', '0018_internalchatsession_internalchatmessage'),
    ]

    operations = [
        migrations.RenameField(
            model_name='internalchatsession',
            old_name='by',
            new_name='session_name',
        ),
        migrations.RemoveField(
            model_name='internalchatmessage',
            name='platform_id',
        ),
    ]
