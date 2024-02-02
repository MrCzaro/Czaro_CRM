# Generated by Django 5.0 on 2024-01-30 07:12

import django.core.validators
import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("patient", "0003_alter_patientobservation_observation"),
        ("scales", "0002_glasgowcomascale"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="NewsScale",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("modified_at", models.DateTimeField(auto_now=True)),
                (
                    "respiratory_rate",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(100),
                        ]
                    ),
                ),
                (
                    "oxygen_saturation",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(100),
                        ]
                    ),
                ),
                (
                    "is_on_oxygen",
                    models.BooleanField(
                        choices=[(True, "Yes"), (False, "No")], default=False
                    ),
                ),
                (
                    "aecopd_state",
                    models.BooleanField(
                        choices=[(True, "Yes"), (False, "No")], default=False
                    ),
                ),
                (
                    "temperature",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=4,
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(50),
                        ],
                    ),
                ),
                (
                    "systolic_blood_pressure",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(300),
                        ]
                    ),
                ),
                (
                    "diastolic_blood_pressure",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(200),
                        ]
                    ),
                ),
                (
                    "heart_rate",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(300),
                        ]
                    ),
                ),
                (
                    "level_of_consciousness",
                    models.CharField(
                        choices=[
                            ("awake", "Awake"),
                            ("verbal", "Patient responds to a verbal stimulus"),
                            ("pain", "Patient responds to a pain stimulus"),
                            ("unresponsive", "Patient is unresponsive to stimulus"),
                        ],
                        default="awake",
                        max_length=60,
                    ),
                ),
                ("total_score", models.IntegerField(blank=True, null=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "patient",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="news",
                        to="patient.patient",
                    ),
                ),
            ],
            options={
                "ordering": ("-created_at",),
            },
        ),
    ]