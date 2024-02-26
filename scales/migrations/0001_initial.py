# Generated by Django 5.0 on 2024-02-25 14:46

import django.core.validators
import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("department", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="BodyMassIndex",
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
                    "body_height",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(300),
                        ]
                    ),
                ),
                (
                    "body_weight",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(400),
                        ]
                    ),
                ),
                (
                    "bmi",
                    models.DecimalField(
                        decimal_places=1,
                        max_digits=4,
                        validators=[django.core.validators.MinValueValidator(0)],
                    ),
                ),
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
        migrations.CreateModel(
            name="GlasgowComaScale",
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
                    "eye_response",
                    models.CharField(
                        choices=[
                            ("4", "Eyes open spontaneously"),
                            ("3", "Eye opening to sound"),
                            ("2", "Eye opening to pain"),
                            ("1", "No eye opening"),
                        ],
                        max_length=30,
                    ),
                ),
                (
                    "verbal_response",
                    models.CharField(
                        choices=[
                            ("5", "Orientated"),
                            ("4", "Confused"),
                            ("3", "Inappropriate words"),
                            ("2", "Incomprehensible sounds"),
                            ("1", "No verbal response"),
                        ],
                        max_length=30,
                    ),
                ),
                (
                    "motor_response",
                    models.CharField(
                        choices=[
                            ("6", "Obeys commands"),
                            ("5", "Localizing pain"),
                            ("4", "Withdrawal from pain"),
                            ("3", "Abnormal flexion to pain"),
                            ("2", "Abnormal extension to pain"),
                            ("1", "No motor response"),
                        ],
                        max_length=30,
                    ),
                ),
                ("total_points", models.IntegerField(blank=True, null=True)),
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
                        decimal_places=1,
                        max_digits=3,
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
                ("score_interpretation", models.TextField()),
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
        migrations.CreateModel(
            name="NortonScale",
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
                    "physical_condition",
                    models.CharField(
                        choices=[
                            ("4", "Good"),
                            ("3", "Fair"),
                            ("2", "Poor"),
                            ("1", "Very Bad"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "mental_condition",
                    models.CharField(
                        choices=[
                            ("4", "Alert"),
                            ("3", "Apathetic"),
                            ("2", "Confused"),
                            ("1", "Stuporous"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "activity",
                    models.CharField(
                        choices=[
                            ("4", "Ambulant"),
                            ("3", "Walks with help"),
                            ("2", "Chairbound"),
                            ("1", "Bedridden"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "mobility",
                    models.CharField(
                        choices=[
                            ("4", "Full"),
                            ("3", "Slightly impared"),
                            ("2", "Very limited"),
                            ("1", "Immobile"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "incontinence",
                    models.CharField(
                        choices=[
                            ("4", "None"),
                            ("3", "Occasional"),
                            ("2", "Usually urinary"),
                            ("1", "Urinary and fecal"),
                        ],
                        max_length=20,
                    ),
                ),
                ("total_points", models.IntegerField(blank=True, null=True)),
                (
                    "pressure_risk",
                    models.CharField(blank=True, max_length=20, null=True),
                ),
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
        migrations.CreateModel(
            name="PainScale",
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
                    "pain_comment",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "pain_level",
                    models.CharField(
                        choices=[
                            ("0", 0),
                            ("1", 1),
                            ("2", 2),
                            ("3", 3),
                            ("4", 4),
                            ("5", 5),
                            ("6", 6),
                            ("7", 7),
                            ("8", 8),
                            ("9", 9),
                            ("10", 10),
                        ],
                        max_length=2,
                    ),
                ),
                ("pain_interpretation", models.TextField()),
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
