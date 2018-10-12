from django.db import models
from django.contrib.auth.models import User

class Profile (models.Model):
    city = models.CharField(max_length=100,blank=True)
    street = models.CharField(max_length=100,blank=True )
    contact =models.CharField(max_length= 100, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="profiles")
