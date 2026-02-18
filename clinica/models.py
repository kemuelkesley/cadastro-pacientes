from django.db import models
from django.core.exceptions import ValidationError
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.

class Contato(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    cpf = models.CharField(max_length=14, unique=True, null=True, verbose_name="CPF")
    data_nascimento = models.DateField(verbose_name="Data de Nascimento")
    celular = PhoneNumberField(region='BR') 
    rua = models.CharField(max_length=40, verbose_name="Rua", blank=True, null=True)
    numero = models.CharField(max_length=10, verbose_name="Número", blank=True, null=True)
    bairro = models.CharField(max_length=30, verbose_name="Bairro", blank=True, null=True)
    cep = models.CharField(max_length=9, verbose_name="CEP", blank=True, null=True)
    estado = models.CharField(max_length=30, verbose_name="Estado", blank=True, null=True)
    uf = models.CharField(max_length=2, verbose_name="UF", blank=True, null=True)

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
    


class Especialidade(models.Model):
    nome = models.CharField(max_length=50, unique=True)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Especialidade"
        verbose_name_plural = "Especialidades"
        ordering = ["nome"]


    def __str__(self):
        return self.nome



class Medico(models.Model):
    nome = models.CharField(max_length=120)
    crm = models.CharField(max_length=20)
    uf_crm = models.CharField(max_length=2)
    email = models.EmailField(blank=True, null=True)
    celular = PhoneNumberField(region='BR')

    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)


    especialidades = models.ManyToManyField(
        "Especialidade",
        through="MedicoEspecialidade",
        related_name="medicos",
    )

    class Meta:
        verbose_name = 'Médico'
        verbose_name_plural = "Médicos"
        ordering = ["nome"]
       
        constraints = [
            models.UniqueConstraint(fields=["crm", "uf_crm"], name="uniq_crm_uf"),
        ]

    def __str__(self):
        return f"{self.nome} (CRM {self.crm}/{self.uf_crm})"




class MedicoEspecialidade(models.Model):
    medico = models.ForeignKey("Medico", on_delete=models.CASCADE)
    especialidade = models.ForeignKey("Especialidade", on_delete=models.CASCADE)

    # Campos extras úteis (opcionais)
    duracao_minutos = models.PositiveIntegerField(default=30)
    valor_consulta = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    principal = models.BooleanField(default=False)

    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name = "Vínculo Médico-Especialidade"
        verbose_name_plural = "Vínculos Médico-Especialidade"
        
        constraints = [
            models.UniqueConstraint(fields=["medico", "especialidade"], name="uniq_medico_especialidade"),
        ]


    def __str__(self):
        return f"{self.medico.nome} - {self.especialidade.nome}"
    








# class Agendamento(models.Model):

#     STATUS_CHOICES = [
#         ('AG', 'Agendado'),
#         ('CA', 'Cancelado'),
#         ('FA', 'Faltou'),
#     ]


 

#     paciente = models.ForeignKey(Contato ,on_delete=models.CASCADE)
#     data_agendamento = models.DateField(verbose_name="Data do Agendamento")
#     hora_agendamento = models.TimeField(verbose_name="Hora do Agendamento")
#     observacao = models.TextField(verbose_name="Observação", blank=True, null=True)
#     status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='AG', verbose_name="Status do Agendamento")

#     criado_em = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.paciente.nome} - {self.data_agendamento} às {self.hora_agendamento.strftime('%H:%M')} ({self.get_status_display()})"
    
class Agendamento(models.Model):
    STATUS_CHOICES = [
        ('AG', 'Agendado'),
        ('CA', 'Cancelado'),
        ('FA', 'Faltou'),
    ]

    paciente = models.ForeignKey("Contato", on_delete=models.CASCADE)
    medico = models.ForeignKey("Medico", on_delete=models.PROTECT)
    especialidade = models.ForeignKey("Especialidade", on_delete=models.PROTECT)

    data_agendamento = models.DateField(verbose_name="Data do Agendamento")
    hora_agendamento = models.TimeField(verbose_name="Hora do Agendamento")

    observacao = models.TextField(verbose_name="Observação", blank=True, null=True)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='AG')

    criado_em = models.DateTimeField(auto_now_add=True)

    def clean(self):
        # Se ainda não tem médico ou especialidade (form incompleto), não tenta validar vínculo
        if not self.medico_id or not self.especialidade_id:
            return

        # 1) valida se médico atende a especialidade
        vinculo_ok = MedicoEspecialidade.objects.filter(
            medico_id=self.medico_id,
            especialidade_id=self.especialidade_id,
            ativo=True,
        ).exists()
        if not vinculo_ok:
            raise ValidationError("Este médico não atende a especialidade selecionada.")

        # 2) conflito simples (mesmo médico, mesma data e hora), ignorando cancelados
        if self.data_agendamento and self.hora_agendamento:
            qs = Agendamento.objects.filter(
                medico_id=self.medico_id,
                data_agendamento=self.data_agendamento,
                hora_agendamento=self.hora_agendamento,
            ).exclude(status="CA")

            if self.pk:
                qs = qs.exclude(pk=self.pk)

            if qs.exists():
                raise ValidationError("Já existe um agendamento para este médico nesse horário.")

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        # Evita quebrar caso alguém tenha instância incompleta em memória (admin/form)
        paciente_nome = getattr(self.paciente, "nome", "—")
        medico_nome = getattr(self.medico, "nome", "—")
        return f"{paciente_nome} - {medico_nome} - {self.data_agendamento} {self.hora_agendamento}"
