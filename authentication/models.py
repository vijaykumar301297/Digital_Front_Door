from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from department.models import Department

# Create your models here.


class ManageAccount(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, username, role, password, **extra_fields):
        values = [email, username]
        field_value_map = dict(zip(self.model.REQUIRED_FIELDS, values))
        for field_name, value in field_value_map.items():
            if not value:
                raise ValueError('The {} value must be set'.format(field_name))

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            username=username,
            role=role,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, username, role, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, username, role, password, **extra_fields)

    def create_superuser(self, email, username, role, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, username, role, password, **extra_fields)


class UserAuthentication(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True, default='')
    first_name = models.CharField(max_length=150, default='')
    last_name = models.CharField(max_length=150, default='')
    email = models.EmailField(unique=True, default='')
    role = models.CharField(max_length=12, default='')
    gender = models.CharField(max_length=12, default='')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, related_name='designation_data')
    designation = models.CharField(max_length=100, null=True)
    phone_number = models.CharField(max_length=15, unique=True, default='')
    address = models.CharField(max_length=150, null=True)
    date_of_birth = models.DateField(max_length=15, blank=False, null=True)
    joining_date = models.DateField(max_length=15, blank=False, null=True)
    about = models.TextField(default='', null=True)
    language_known = models.TextField(default='', null=True)
    education = models.TextField(default='', null=True)
    experience = models.CharField(max_length=100,default='', null=True)
    img = models.FileField(upload_to="uploads/", default='')
    account_status = models.CharField(max_length=10, null=True)
    is_superuser = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(null=True)
    location = models.CharField(max_length=255, null=True)
    linkedin = models.TextField(max_length=100,default='', null=True)
    license_no = models.CharField(max_length=100,default='', null=True)
    emp_id = models.CharField(max_length=10, default='', null=True)
    objects = ManageAccount()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email', 'role','phone_number', 'account_status']

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username.split()[0]



