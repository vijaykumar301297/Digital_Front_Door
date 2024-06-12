from django.db import models
from authentication.models import UserAuthentication


# Create your models here.

class Patient(models.Model):
    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, unique=True, default='')
    email = models.EmailField(max_length=100, unique=True, default='')
    date_of_birth = models.DateField(max_length=15, blank=False, null=True)
    gender = models.CharField(max_length=12, default='')
    user_id = models.ForeignKey(UserAuthentication, on_delete=models.CASCADE, null=True, related_name='doctor')
    specialization = models.CharField(max_length=120, default='')
    location = models.CharField(max_length=120, default='')
    dates = models.DateField(max_length=12, default='')
    appointed_date = models.CharField(max_length=12, default='')
    payment = models.CharField(max_length=12)

