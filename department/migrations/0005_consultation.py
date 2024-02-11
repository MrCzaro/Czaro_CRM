# Generated by Django 5.0 on 2024-02-11 05:35

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("department", "0004_vitalsigns_hospitalization_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Consultation",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("consultation_name", models.CharField(max_length=255)),
                ("consultation", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("modified_at", models.DateTimeField(auto_now=True, null=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "hospitalization",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="department.hospitalization",
                    ),
                ),
            ],
            options={
                "ordering": ("-created_at",),
            },
        ),
    ]