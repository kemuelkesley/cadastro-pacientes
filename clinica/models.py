from django.db import models

from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User

from django.utils import timezone


# Create your models here.

class Contato(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    data_nascimento = models.DateField()
    celular = PhoneNumberField(region='BR')  # Defina a região como Brasil

    ativo = models.BooleanField(default=True)
    data_exclusao = models.DateField(null=True, blank=True)
    usuario_exclusao = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='contatos_excluidos'
    )

    def marcar_como_inativo(self, usuario):
        self.ativo = False
        self.data_exclusao = timezone.now()
        self.usuario_exclusao = usuario
        self.save()
    

    def __str__(self):
        return self.nome
    
