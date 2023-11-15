from django.contrib import admin
from clinica.models import Contato

# Register your models here.

class ContatoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'email',)
    list_per_page = 10
    
  
   
   


admin.site.register(Contato, ContatoAdmin)
