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
    contact_firstname = models.CharField(max_length=30)
    contact_lastname = models.CharField(max_length=30)
    contact_relationship = models.CharField(max_length=30)
    contact_email = models.CharField(max_length=255)
    contact_mobile = models.CharField(max_length=30)
    contact_facebook = models.CharField(max_length=60)
    contact_city = models.CharField(max_length=60)
    contact_state = models.CharField(max_length=2)
    alert_email = models.BooleanField(default=False)
    alert_text = models.BooleanField(default=False)
    alert_facebook = models.BooleanField(default=False)
    mobile_carrier = models.IntegerField(max_length=1, choices=CARRIERS)
    user = models.ForeignKey(User)

