from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.

class Contato(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    data_nascimento = models.DateField(verbose_name="Data de Nascimento")
    celular = PhoneNumberField(region='BR') 

    ativo = models.BooleanField(default=True)
    data_criacao = models.DateTimeField(verbose_name="Data de Criação", auto_now_add=True)
    usuario_criacao = models.ForeignKey(
        User, 
        verbose_name="Quem criou?", 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
    )
    data_exclusao = models.DateTimeField(verbose_name="Data de Exclusão",null=True, blank=True)
    usuario_exclusao = models.ForeignKey(
        User, 
        verbose_name="Quem excluiu?",
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
    

class Agendamento(models.Model):
    paciente = models.ForeignKey(Contato ,on_delete=models.CASCADE)
    data_agendamento = models.DateField(verbose_name="Data do Agendamento")
    hora_agendamento = models.TimeField(verbose_name="Hora do Agendamento")
    observacao = models.TextField(verbose_name="Observação", blank=True, null=True)

    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.paciente.nome} - {self.data_agendamento} às {self.hora_agendamento.strftime('%H:%M')}"