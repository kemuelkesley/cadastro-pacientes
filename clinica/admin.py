from django.contrib import admin
from clinica.models import Contato, Agendamento

# Register your models here.

class ContatoAdmin(admin.ModelAdmin):
    list_display = ('id', 
    'nome', 
    'email', 
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
    'criado_em',
    )

    
    list_display_links = ('id', 'paciente',)
    list_per_page = 10


admin.site.register(Contato, ContatoAdmin)
admin.site.register(Agendamento, AgendamentoAdmin)