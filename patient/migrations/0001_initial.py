# Generated by Django 5.0 on 2024-02-25 14:46

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Patient",
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
                ("first_name", models.CharField(max_length=255)),
                ("last_name", models.CharField(max_length=255)),
                ("date_of_birth", models.DateField()),
                ("contact_number", models.CharField(max_length=15)),
                (
                    "is_insured",
                    models.BooleanField(
                        choices=[(True, "Yes"), (False, "No")], default=True
                    ),
                ),
                ("insurance", models.CharField(max_length=255)),
                ("country", models.CharField(max_length=255)),
                ("city", models.CharField(max_length=255)),
                ("street", models.CharField(max_length=255)),
                ("zip_code", models.CharField(max_length=255)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("modified_at", models.DateTimeField(auto_now=True, null=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
