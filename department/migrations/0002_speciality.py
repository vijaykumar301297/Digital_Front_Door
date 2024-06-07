# Generated by Django 5.0.3 on 2024-05-30 10:01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("department", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Speciality",
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
                ("speciality", models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
    ]
