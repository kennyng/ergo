from django.db import models
from django.contrib.auth.models import User
from django_extensions.db.fields import UUIDField


class UserProfile(models.Model):
    profile_id = models.AutoField(primary_key=True)
    ergo_id = UUIDField(version=4, unique=True)
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    dob = models.DateField()
    sex = models.CharField(max_length=6)
    blood_type = models.CharField(max_length=3, blank=True, null=True)
    organ_donor = models.BooleanField(default=False)
    phone = models.CharField(max_length=12)
    address = models.CharField(max_length=120)
    city = models.CharField(max_length=60)
    state = models.CharField(max_length=2)
    zipcode = models.CharField(max_length=10)
    profile_img = models.ImageField(upload_to='profile_pics/%Y/%m/%d')
    user = models.ForeignKey(User)
