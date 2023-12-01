from django.db import models
#import phonenumbers

from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.

class Contato(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    data_nascimento = models.DateField()
    celular = PhoneNumberField(region='BR')  # Defina a região como Brasil

    

    def __str__(self):
        return self.nome
    
