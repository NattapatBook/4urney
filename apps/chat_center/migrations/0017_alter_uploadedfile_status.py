# Generated by Django 5.1.4 on 2025-01-16 04:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat_center', '0016_uploadedfile_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadedfile',
            name='status',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
