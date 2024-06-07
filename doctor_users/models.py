from django.db import models
from department.models import Department
from authentication.models import UserAuthentication


# Create your models here.

class ScheduleTime(models.Model):
    deptId = models.ForeignKey(Department,  on_delete=models.CASCADE, null=True, related_name='department')
    user_id = models.ForeignKey(UserAuthentication, on_delete=models.CASCADE, null=True, related_name='doctor_id')
    date = models.DateField(max_length=15, blank=False, null=True)
    from_time = models.CharField(max_length=15,blank=False, null=True)
    to_time = models.CharField(max_length=15,blank=False, null=True)
    location = models.CharField(max_length=15,blank=False, null=True)
    availability = models.CharField(max_length=15,blank=False, null=True)
