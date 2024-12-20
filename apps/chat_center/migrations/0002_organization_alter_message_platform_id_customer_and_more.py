# Generated by Django 5.1 on 2024-11-26 12:51

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        ("chat_center", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Organization",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AlterField(
            model_name="message",
            name="platform_id",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.CreateModel(
            name="Customer",
            fields=[
                (
                    "platform_id",
                    models.CharField(
                        max_length=1000, primary_key=True, serialize=False
                    ),
                ),
                ("img", models.CharField(blank=True, max_length=1000, null=True)),
                ("name", models.CharField(blank=True, max_length=1000, null=True)),
                ("tag", models.CharField(blank=True, max_length=1000, null=True)),
                ("priority", models.CharField(blank=True, max_length=1000, null=True)),
                (
                    "lastest_msg",
                    models.CharField(blank=True, max_length=1000, null=True),
                ),
                ("timestamp", models.DateTimeField(blank=True, null=True)),
                ("is_urgent", models.BooleanField(blank=True, null=True)),
                ("provider", models.CharField(blank=True, max_length=1000, null=True)),
                ("agent", models.CharField(blank=True, max_length=1000, null=True)),
                (
                    "message_type",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "reply_token",
                    models.CharField(blank=True, max_length=1000, null=True),
                ),
                (
                    "organization_id",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="chat_center.organization",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="message",
            name="organization_id",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="chat_center.organization",
            ),
        ),
        migrations.CreateModel(
            name="OrganizationMember",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "group",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="auth.group",
                    ),
                ),
                (
                    "organization",
                    models.ForeignKey(
                        blank=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="chat_center.organization",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.DeleteModel(name="User",),
    ]
