# Generated by Django 5.1.3 on 2025-01-06 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat_center', '0008_routingchain'),
    ]

    operations = [
        migrations.AddField(
            model_name='routingchain',
            name='is_active',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]