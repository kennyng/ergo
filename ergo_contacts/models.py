from django.db import models
from django.contrib.auth.models import User


class Contact(models.Model):
    CARRIERS = (
        (0, 'other'),
        (1, 'att'),
        (2, 'verizon'),
        (3, 'tmobile'),
        (4, 'sprint'),
        (5, 'virgin'),
    )

    contact_id = models.AutoField(primary_key=True)
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    relationship = models.CharField(max_length=30, blank=True)
    email = models.CharField(max_length=255, blank=True)
    mobile = models.CharField(max_length=30, blank=True)
    facebook = models.CharField(max_length=60, blank=True)
    city = models.CharField(max_length=60, blank=True)
    state = models.CharField(max_length=2, blank=True)
    alert_email = models.BooleanField(default=False)
    alert_text = models.BooleanField(default=False)
    alert_fb = models.BooleanField(default=False)
    mobile_carrier = models.IntegerField(max_length=1, choices=CARRIERS, blank=True)
    user = models.ForeignKey(User)

