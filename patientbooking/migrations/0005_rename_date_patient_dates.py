# Generated by Django 5.0.4 on 2024-06-04 09:22

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        (
            "patientbooking",
            "0004_alter_patient_appointed_date_alter_patient_location_and_more",
        ),
    ]

    operations = [
        migrations.RenameField(
            model_name="patient",
            old_name="date",
            new_name="dates",
        ),
    ]
