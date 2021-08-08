from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    university = models.ForeignKey("University", blank=True, null=True, on_delete=models.SET_NULL)
    fieldstudy = models.ForeignKey("FieldStudy", blank=True, null=True, on_delete=models.SET_NULL)
    email_confirmed = models.BooleanField(default=False)

class University(models.Model):
    name = models.CharField(max_length=250)
    bio = models.TextField(blank=True, null=True, default=None)


class FieldStudy(models.Model):
    name = models.CharField(max_length=250)

