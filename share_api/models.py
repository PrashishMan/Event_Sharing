from django.db import models

# Create your models here.
class User (models.Model):
    firstName = models.CharField(max_length= 100)
    lastName = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    contact =models.CharField(max_length= 100)
    email =models.EmailField()

    def __str__(self):
        return print("First name : " + self.firstName + " Last Name : " + self.lastName)
