# Generated by Django 5.0 on 2024-02-19 09:26

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("department", "0005_consultation"),
    ]

    operations = [
        migrations.AlterField(
            model_name="department",
            name="name",
            field=models.CharField(
                max_length=255,
                unique=True,
                validators=[django.core.validators.MinLengthValidator(1)],
            ),
        ),
    ]
