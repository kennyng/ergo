from django.db import models
from django.contrib.auth.models import User
from django_extensions.db.fields import UUIDField

import os.path


def get_image_path(instance, filename):
    return os.path.join('users', str(instance.id), filename)

def get_thumbnail_path(instance, filename):
    return os.path.join('users', str(instance.id), 'thumbnail', filename)


class ProfileImage(models.Model):
    user = models.ForeignKey(User, unique=True)
    image = models.ImageField(upload_to=get_image_path, blank=True, null=True)
    thumbnail = models.ImageField(upload_to=get_thumbnail_path, blank=True, null=True)


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
    user = models.OneToOneField(User)
