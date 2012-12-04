from django.db import models
from django.contrib.auth.models import User


class Allergy(models.Model):
    ALLERGY_TYPES = (
        (0, 'Drug'),
        (1, 'Misc.'),
    )

    allergy_id = models.AutoField(primary_key=True)
    category = models.IntegerField(max_length=1, choices=ALLERGY_TYPES)
    name = models.CharField(max_length=60)
    image = models.CharField(max_length=60)
    users = models.ManyToManyField(User, through='UserToAllergy')
    
class UserToAllergy(models.Model):
    ALLERGY_TYPES = (
        (0, 'Drug'),
        (1, 'Misc.'),
    )
    
    user = models.ForeignKey(User)
    allergy = models.ForeignKey(Allergy)
    category = models.IntegerField(max_length=1, choices=ALLERGY_TYPES)
    date_added = models.DateTimeField(auto_now_add=True)
    
class Drug(models.Model):
    DRUG_TYPES = (
        (0, 'Prescription'),
        (1, 'OTC'),
        (2, 'Misc.'),
    )

    drug_id = models.AutoField(primary_key=True)
    category = models.IntegerField(max_length=1, choices=DRUG_TYPES)
    name = models.CharField(max_length=60)
    image = models.CharField(max_length=60)
    users = models.ManyToManyField(User, through='UserToDrug')
    
class UserToDrug(models.Model):
    DRUG_TYPES = (
        (0, 'Prescription'),
        (1, 'OTC'),
        (2, 'Misc.'),
    )

    user = models.ForeignKey(User)
    drug = models.ForeignKey(Drug)
    category = models.IntegerField(max_length=1, choices=DRUG_TYPES)
    date_added = models.DateTimeField(auto_now_add=True)
    
class Immunization(models.Model):
    vaccine_id = models.AutoField(primary_key=True)
    vaccine_name = models.CharField(max_length=60)
    users = models.ManyToManyField(User, through='UserToImmunization')
    
class UserToImmunization(models.Model):
    user = models.ForeignKey(User)
    vaccine = models.ForeignKey(Immunization)
    vaccine_date = models.DateField()
    date_added = models.DateTimeField(auto_now_add=True)
    
class History(models.Model):
    HISTORY_TYPES = (
        (0, 'Condition'),
        (1, 'Accident'),
        (2, 'Surgery'),
        (3, 'Visit'),
    )
    
    history_id = models.AutoField(primary_key=True)
    date = models.DateField()
    category = models.IntegerField(max_length=1, choices=HISTORY_TYPES)
    description = models.CharField(max_length=140)
    date_added = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User)
    
class FamilyHistory(models.Model):
    family_id = models.AutoField(primary_key=True)
    relationship = models.CharField(max_length=60)
    condition = models.CharField(max_length=140)
    date_added = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User)
    
class Provider(models.Model):
    provider_id = models.AutoField(primary_key=True)
    insurance_name = models.CharField(max_length=60)
    group_num = models.CharField(max_length=30)
    policy_num = models.CharField(max_length=30)
    insurance_contact = models.CharField(max_length=30)
    pcp_name = models.CharField(max_length=60)
    pcp_contact = models.CharField(max_length=30)
    pcp_location = models.CharField(max_length=80)
    pcp_address = models.CharField(max_length=120)
    pcp_city = models.CharField(max_length=60)
    pcp_state = models.CharField(max_length=2)
    pcp_zipcode = models.CharField(max_length=10)
    user = models.ForeignKey(User)
