from django.db import models


class Department(models.Model):
    department_name = models.CharField(max_length=100, blank=False, null=True)
    department_no = models.CharField(max_length=100, blank=False, null=True)
    department_head = models.CharField(max_length=100, blank=False, null=True)
    department_date = models.DateField(max_length=15, blank=False, null=True)
    department_status = models.CharField(max_length=100, default='Active')
    department_info = models.TextField(max_length=1000, blank=False, null=True)

    def __str__(self):
        return self.department_name


class Speciality(models.Model):
    speciality = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.speciality
