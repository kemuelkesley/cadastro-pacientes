from urllib import request
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from .forms import ContatoForm
from .models import Contato
from django.core.paginator import Paginator

from django.views.generic import ListView, UpdateView
from django.shortcuts import get_object_or_404
from django.urls import reverse

# Create your views here.


class ClinicaListView(ListView):
    model = Contato
    template_name = 'clinica/clinica_list.html'
    context_object_name = 'clinica_list'
    paginate_by = 10  

    def get_queryset(self):
        return Contato.objects.all().order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Configuração do Paginator
        lista_paginator = Paginator(context['clinica_list'], self.paginate_by)
        page_num = self.request.GET.get('page')
        page = lista_paginator.get_page(page_num)
        
        context['clinica_list'] = page
        context['lista_paginator'] = lista_paginator

        return context
    

class ClinicaUpdateView(UpdateView):
    model = Contato
    fields = ['nome', 'email']       
    success_url = reverse_lazy('clinica_list')
    template_name = 'clinica/contato_form.html'
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['nome'].widget.attrs['class'] = 'form-control'
        form.fields['email'].widget.attrs['class'] = 'form-control'
        return form
   

# def cadastro(request):
#     if request.method == 'POST':
#         form = ContatoForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('sucesso')  
#     else:
#         form = ContatoForm()

#     return render(request, 'clinica/contato_form.html', {'form': form})


from django.urls import reverse

def cadastro(request):
    if request.method == 'POST':
        form = ContatoForm(request.POST)
        if form.is_valid():
            form.save()
            novo_contato = form.save(commit=False)  # Evita salvar no banco antes de associar o objeto
            novo_contato.save()  # Agora salva o objeto
            return redirect(reverse('sucesso'))
    else:
        form = ContatoForm()

    return render(request, 'clinica/contato_form.html', {'form': form})




def sucesso(request):
    return render(request, 'clinica/sucesso.html')


