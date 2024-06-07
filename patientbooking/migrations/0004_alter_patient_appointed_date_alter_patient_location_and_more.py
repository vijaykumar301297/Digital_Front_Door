# Generated by Django 5.0.4 on 2024-06-04 09:19

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("patientbooking", "0003_alter_patient_appointed_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="patient",
            name="appointed_date",
            field=models.CharField(default="", max_length=12),
        ),
        migrations.AlterField(
            model_name="patient",
            name="location",
            field=models.CharField(default="", max_length=120),
        ),
        migrations.AlterField(
            model_name="patient",
            name="specialization",
            field=models.CharField(default="", max_length=120),
        ),
    ]