# Generated by Django 4.0.6 on 2024-06-11 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userauthentication',
            name='phone_number',
            field=models.CharField(default='', max_length=20, unique=True),
        ),
    ]