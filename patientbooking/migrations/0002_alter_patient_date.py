# Generated by Django 5.0.4 on 2024-06-04 09:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("patientbooking", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="patient",
            name="date",
            field=models.DateField(default="", max_length=12),
        ),
    ]
