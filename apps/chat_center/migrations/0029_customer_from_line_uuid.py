# Generated by Django 5.1.3 on 2025-02-24 11:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat_center', '0028_requestdemo'),
        ('webhook_line', '0008_lineintegration_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='from_line_uuid',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='webhook_line.lineintegration'),
        ),
    ]
