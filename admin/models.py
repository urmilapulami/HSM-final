from django.db import models

# Create your models here.<!-- accounts/models.py -->
from django.contrib.auth.models import AbstractUser,UserManager

class ModelUser(UserManager):
    ...

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", 1)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username, email, password, **extra_fields)

    def create_student(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("role", 2)
        return self._create_user(username, email, password, **extra_fields)
    
    def create_employee(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("role", 3)
        return self._create_user(username, email, password, **extra_fields)
    
class User(AbstractUser):
    mobile_number = models.CharField(max_length=20, null=True)
    address = models.CharField(max_length=300, null=True)
    role = models.IntegerField(max_length=20, null=True)
    gender = models.CharField(max_length=10, default="unknown")
    image = models.FileField(upload_to='documents',null=True,blank=True)
    objects = ModelUser()

class Hostel(models.Model):
    name = models.CharField(max_length=200)
    note = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name

class Room(models.Model):
    name = models.CharField(max_length=200)
    floor = models.CharField(max_length=200, null=True)
    note = models.CharField(max_length=200, null=True)
    user = models.OneToOneField(
        User,
        on_delete=models.PROTECT,null=True
    )
    date = models.CharField(max_length=200, null=True)
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

class Meal(models.Model):
    day = models.CharField(max_length=200)
    breakfast = models.CharField(max_length=200, null=True)
    lunch = models.CharField(max_length=200, null=True)
    dinner = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.day

class RoomChange(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,null=True
    )
    room = models.OneToOneField(
        Room,
        on_delete=models.CASCADE,null=True
    )
    status = models.CharField(max_length=200, default="Requested")

class Notice(models.Model):
    user = models.CharField(max_length=200, null=True,blank=True)
    date = models.CharField(max_length=200)
    notice = models.CharField(max_length=1000, null=True)

    def __str__(self):
        return self.notice
class Billing(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,null=True,unique=False
    )
    date = models.DateField(max_length=200)
    amount = models.IntegerField(null=True)
    remark = models.CharField(max_length=1000, null=True)

    def __str__(self):
        return self.notice