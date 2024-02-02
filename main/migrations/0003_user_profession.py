# Generated by Django 5.0 on 2024-01-31 05:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0002_remove_user_name_user_first_name_user_last_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="profession",
            field=models.CharField(
                choices=[
                    ("nurses", "Nurse"),
                    ("physicians", "Physician"),
                    ("secretaries", "Secretary"),
                ],
                default=1,
                max_length=50,
            ),
            preserve_default=False,
        ),
    ]