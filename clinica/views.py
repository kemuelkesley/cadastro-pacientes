from django.http import HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from .forms import ContatoForm
from .models import Contato
from django.core.paginator import Paginator
from django.contrib import messages
from django.views.generic import ListView, UpdateView
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe

from django.db.models import Q
from .validators import validate_nome, validate_celular, validate_data_nascimento


# usado para criar pesquisa na pagina
def buscar_contatos(nome):
    if nome:
        return Contato.objects.filter(
            Q(nome__icontains=nome) | Q(email__icontains=nome)
        )

    else:
        return Contato.objects.all()


def criar_paginacao(request, objeto):
    paginator = Paginator(objeto, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return page_obj


class ClinicaListView(ListView):
    model = Contato
    template_name = "clinica/clinica_list.html"
    context_object_name = "clinica_list"

    def get_queryset(self):
        nome = self.request.GET.get("nome", None)
        return buscar_contatos(nome).filter(ativo=True)
        # return buscar_contatos(nome)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        objeto = self.get_queryset()
        page_obj = criar_paginacao(self.request, objeto)
        context["page_obj"] = page_obj
        context["criar_paginacao"] = criar_paginacao(
            self.request, Contato.objects.all()
        )  # Use uma consulta diferente para a paginação

        return context


#  success_message = messages.get_messages(self.request)
#         if success_message:
#             context['success_message'] = success_message


class ClinicaUpdateView(UpdateView):
    model = Contato
    fields = ["nome", "email", "data_nascimento", "celular"]
    success_url = reverse_lazy("clinica_list")
    template_name = "clinica/editar_contato.html"

    # tem um certo controle no formulario de editar contato
    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        # Adiciona validador customizado ao campo "nome"
        form.fields["nome"].validators.append(validate_nome)
        form.fields["celular"].validators.append(validate_celular)
        form.fields["data_nascimento"].validators.append(validate_data_nascimento)

        # Adiciona classes CSS aos campos do formulário
        form.fields["nome"].widget.attrs["class"] = "form-control custom-input"
        form.fields["email"].widget.attrs["class"] = "form-control custom-input"
        form.fields["data_nascimento"].widget.attrs[
            "class"
        ] = "form-control custom-input"
        form.fields["celular"].widget.attrs["class"] = "form-control custom-input"
        return form

    def form_valid(self, form):
        messages.success(
            self.request,
            mark_safe(
                f'Paciente <a href="{reverse("clinica_update", kwargs={"pk": self.object.pk})}" class="text-primary">{self.object.nome}</a> Atualizado com sucesso!'
            ),
        )
        return super().form_valid(form)

# def deletar_contato(request, pk):
#     contato = get_object_or_404(Contato, pk=pk)
#     contato.delete()
#     return redirect('clinica_list')


# Metodo funcionando apagando direto do banco de dados
# def deletar_contato(request, pk):
#     if request.method == 'GET':
#         contato = get_object_or_404(Contato, pk=pk)
#         return render(request, 'clinica/confirmar_exclusao_contato.html', {'contato': contato})

#     elif request.method == 'POST':
#         contato = get_object_or_404(Contato, pk=pk)
#         contato.delete()
#         return redirect('clinica_list')

#     else:
#         return HttpResponseNotAllowed(['POST'])


# Metodo que faz uma exclusao logica ou seja não apaga do banco e deixa o paciente inativo.
def deletar_contato(request, pk):
    contato = get_object_or_404(Contato, pk=pk)

    if request.method == "GET":
        return render(
            request, "clinica/confirmar_exclusao_contato.html", {"contato": contato}
        )

    elif request.method == "POST":
        # Atualize o campo 'ativo' para False em vez de excluir o contato
        # contato.ativo = False
        # contato.save()
        contato.marcar_como_inativo(request.user)

        messages.warning(request, f"Paciente {contato.nome} excluído com sucesso!", extra_tags='excluído')
        return redirect("clinica_list")

    else:
        return HttpResponseNotAllowed(["POST"])


@login_required
def cadastro(request):
    if request.method == "POST":
        form = ContatoForm(request.POST)
        if form.is_valid():
            form.save()
            novo_contato = form.save(commit=False)  # Evita salvar no banco antes de associar o objeto
            novo_contato.save()

            #messages.success(request, f"Paciente {novo_contato.nome} cadastrado com sucesso!")

            messages.success(
                request, 
                mark_safe(f'Paciente <a href="{reverse("clinica_update", kwargs={"pk": novo_contato.pk})}" class="text-primary">{novo_contato.nome}</a> cadastrado com sucesso!'))

            return redirect("clinica_list")
    else:
        form = ContatoForm()

    return render(request, "clinica/contato_form.html", {"form": form})


def sucesso(request):
    return render(request, "clinica/sucesso.html")
