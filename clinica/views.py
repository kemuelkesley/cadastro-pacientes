from urllib import request
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from .forms import ContatoForm
from .models import Contato
from django.core.paginator import Paginator

from django.views.generic import ListView, UpdateView
from django.urls import reverse
from django.db.models import Q


# usado para criar pesquisa na pagina
def buscar_contatos(nome):
    if nome:
        return Contato.objects.filter(Q(nome__icontains=nome) | Q(email__icontains=nome))
    
    else:        
        return Contato.objects.all()
    

def criar_paginacao(request, objeto):
    paginator = Paginator(objeto, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return page_obj



class ClinicaListView(ListView):
    model = Contato
    template_name = 'clinica/clinica_list.html'
    context_object_name = 'clinica_list'      

       
    def get_queryset(self):
        nome = self.request.GET.get('nome', None)
        return buscar_contatos(nome)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        objeto = self.get_queryset()
        page_obj = criar_paginacao(self.request, objeto)
        context['page_obj'] = page_obj
        context['criar_paginacao'] = criar_paginacao(self.request, Contato.objects.all())  # Use uma consulta diferente para a paginação
        return context


class ClinicaUpdateView(UpdateView):
    model = Contato
    fields = ['nome', 'email', 'data_nascimento', 'celular']       
    success_url = reverse_lazy('clinica_list')
    template_name = 'clinica/editar_contato.html'
    


    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['nome'].widget.attrs['class'] = 'form-control'
        form.fields['email'].widget.attrs['class'] = 'form-control'
        form.fields['data_nascimento'].widget.attrs['class'] = 'form-control'
        form.fields['celular'].widget.attrs['class'] = 'form-control'
        return form
   

    
    def get_success_url(self):
        return reverse_lazy('clinica_list')


# def cadastro(request):
#     if request.method == 'POST':
#         form = ContatoForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('sucesso')  
#     else:
#         form = ContatoForm()

#     return render(request, 'clinica/contato_form.html', {'form': form})






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


