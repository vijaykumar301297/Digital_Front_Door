from django.db import models


# Create your models here.
class Staff(models.Model):
    first_name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=50, null=False)
    department = models.CharField(max_length=50, null=False)
    role = models.CharField(max_length=50, null=False)
    designation = models.CharField(max_length=50, null=False)

    # first_name = models.CharField(max_length=50, null=False)

    def __str__(self):
        return self.first_name
