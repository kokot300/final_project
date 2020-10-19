from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class UserProfile(models.Model):
    phone = models.IntegerField()
    birth_date = models.DateField()
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)


class Address(models.Model):
    name = models.CharField(max_length=63)
    address_line_1 = models.CharField(max_length=123)
    address_line_2 = models.CharField(max_length=123)
    city = models.CharField(max_length=63)
    zip_code = models.IntegerField()
    country = models.CharField(max_length=31)
    profile = models.ForeignKey(to=UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
