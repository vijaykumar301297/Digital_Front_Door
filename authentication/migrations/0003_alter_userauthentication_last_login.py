# Generated by Django 5.0.4 on 2024-06-03 06:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("authentication", "0002_alter_userauthentication_last_login"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userauthentication",
            name="last_login",
            field=models.DateTimeField(null=True),
        ),
    ]
