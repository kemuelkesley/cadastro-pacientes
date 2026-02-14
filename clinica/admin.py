from django.contrib import admin
from clinica.models import Contato, Agendamento, Especialidade, Medico, MedicoEspecialidade

# Register your models here.

class ContatoAdmin(admin.ModelAdmin):
    list_display = ('id', 
    'nome', 
    'email', 
    'cpf',
    'data_nascimento', 
    'celular', 
    'data_criacao',
    'usuario_criacao',
    'data_exclusao', 
    'usuario_exclusao',
    'ativo',
    )

    list_display_links = ('id', 'nome',)
    search_fields = ('nome',)
    list_per_page = 10
    


class AgendamentoAdmin(admin.ModelAdmin):
    list_display = ('id', 
    'paciente', 
    'data_agendamento', 
    'hora_agendamento', 
    'observacao',
    'status',
    'criado_em',
    )

    
    list_display_links = ('id', 'paciente',)
    list_per_page = 10



@admin.register(Especialidade)
class EspecialidadeAdmin(admin.ModelAdmin):
    list_display = ("nome", "ativo", "criado_em")
    search_fields = ("nome",)
    list_filter = ("ativo",)
    ordering = ("nome",)  # aqui só campo de Especialidade


class MedicoEspecialidadeInline(admin.TabularInline):
    model = MedicoEspecialidade
    extra = 1

    # campos do MODEL MedicoEspecialidade
    fields = ("especialidade", "duracao_minutos", "valor_consulta", "principal", "ativo")

    # autocomplete funciona bem para ForeignKey
    autocomplete_fields = ("especialidade",)

    # ordenação do inline (usa campos do MedicoEspecialidade e/ou relação)
    ordering = ("-principal", "especialidade__nome")


@admin.register(Medico)
class MedicoAdmin(admin.ModelAdmin):
    list_display = ("nome", "crm", "uf_crm", "email", "ativo", "criado_em")
    search_fields = ("nome", "crm", "email")
    list_filter = ("ativo", "uf_crm")
    ordering = ("nome",)

    inlines = [MedicoEspecialidadeInline]


@admin.register(MedicoEspecialidade)
class MedicoEspecialidadeAdmin(admin.ModelAdmin):
    list_display = ("medico", "especialidade", "duracao_minutos", "valor_consulta", "principal", "ativo", "criado_em")
    search_fields = ("medico__nome", "medico__crm", "especialidade__nome")
    list_filter = ("ativo", "principal", "especialidade")
    ordering = ("medico__nome", "especialidade__nome")

    autocomplete_fields = ("medico", "especialidade")







admin.site.register(Contato, ContatoAdmin)
admin.site.register(Agendamento, AgendamentoAdmin)