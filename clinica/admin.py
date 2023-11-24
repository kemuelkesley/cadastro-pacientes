from django.contrib import admin
from clinica.models import Contato

# Register your models here.

class ContatoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'email', 'data_nascimento', 'celular',)
    list_display_links = ('id', 'nome',)
    search_fields = ('nome',)
    list_per_page = 10
    


admin.site.register(Contato, ContatoAdmin)
