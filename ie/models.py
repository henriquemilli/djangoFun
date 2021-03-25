from unittest.case import skip
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField




class Csv(models.Model):
    file = models.FileField()
    uploaded = models.DateTimeField(auto_now_add=True)



class PulledCsv(models.Model):
    name = models.CharField(max_length=18)
    timestamp = models.IntegerField()



class Cliente(models.Model):
    azienda = models.CharField(max_length=18)
    email = models.EmailField(max_length=18)
    telefono = PhoneNumberField()
    importunato = models.BooleanField(default=False)