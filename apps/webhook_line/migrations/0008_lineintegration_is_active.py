# Generated by Django 5.1.3 on 2025-02-20 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webhook_line', '0007_lineintegration_connected_on'),
    ]

    operations = [
        migrations.AddField(
            model_name='lineintegration',
            name='is_active',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
