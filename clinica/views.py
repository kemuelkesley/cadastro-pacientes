import datetime
import json
from django.http import HttpResponseNotAllowed, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from .forms import AgendamentoForm, ContatoForm, CadastroForm, MedicoForm
from .models import Contato, Especialidade, Medico, MedicoEspecialidade
from django.core.paginator import Paginator
from django.views.generic import ListView, UpdateView
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
from django.views.decorators.http import require_POST
from django.views.decorators.http import require_GET


from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views.generic import ListView
from django.core.paginator import Paginator
from clinica.models import Contato, Agendamento
from django.utils.timezone import now
import datetime


# Autenticação
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout



from django.db.models import Q
from .validators import validate_nome, validate_celular, validate_data_nascimento

# Acessar se estiver logado no sistema
from django.contrib.auth.mixins import LoginRequiredMixin

# import de mensagem de sucesso
from django.contrib import messages




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


class ClinicaListView(LoginRequiredMixin,ListView):
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



class ClinicaUpdateView(UpdateView):
    model = Contato
    fields = ["nome", "email", "cpf", "data_nascimento", "celular", "cep", "rua", "numero", "bairro", "estado", "uf"]
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
        form.fields["cpf"].widget.attrs["class"] = "form-control custom-input"
        form.fields["data_nascimento"].widget.attrs["class"] = "form-control custom-input"
        form.fields["celular"].widget.attrs["class"] = "form-control custom-input"
        form.fields["cep"].widget.attrs["class"] = "form-control custom-input"
        form.fields["rua"].widget.attrs["class"] = "form-control custom-input"
        form.fields["numero"].widget.attrs["class"] = "form-control custom-input"
        form.fields["bairro"].widget.attrs["class"] = "form-control custom-input"
        form.fields["estado"].widget.attrs["class"] = "form-control custom-input"
        form.fields["uf"].widget.attrs["class"] = "form-control custom-input"

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
            novo_contato = form.save(commit=False)
            novo_contato.usuario_criacao = request.user
            novo_contato.save()
            
            messages.success(
                request, 
                mark_safe(f'Paciente <a href="{reverse("clinica_update", kwargs={"pk": novo_contato.pk})}" class="text-primary">{novo_contato.nome}</a> cadastrado com sucesso!'))

            return redirect("clinica_list")
    else:
        form = ContatoForm()
    return render(request, "clinica/contato_form.html", {"form": form})


def sucesso(request):
    return render(request, "clinica/sucesso.html")


######################### Cadastro de usuario no sitemas e login #############################

def cadastrar_usuario(request):
    if request.method == "POST":
        form_usuario = CadastroForm(request.POST)  # Use CadastroForm em vez de UserCreationForm
        if form_usuario.is_valid():
            form_usuario.save()
            messages.success(request, 'Sua conta foi criada com sucesso. Faça login para continuar.')
            return redirect('cadastrar_usuario')
    else:
        form_usuario = CadastroForm()
    return render(request, 'login/cadastro.html', {'form_usuario': form_usuario})



def logar_usuario(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        usuario = authenticate(request, username=username, password=password)
        if usuario is not None:
            login(request, usuario)
            return redirect('index')
        else:
            messages.error(request, 'Usuário ou senha incorretos. Por favor, tente novamente.')
   
    form_login = AuthenticationForm()
    return render(request, 'login/login.html', {'form_login': form_login})



def deslogar_usuario(request):
    logout(request)
    return redirect('logar_usuario')


@login_required
def index(request):
    return render(request, 'login/index.html')


@login_required
def agendar_consulta(request):
    if request.method == "POST":
        form = AgendamentoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Consulta agendada com sucesso!')
            return redirect('listar_agendamentos')  
    else:
        form = AgendamentoForm()
    
    return render(request, 'agendamento/agendamento.html', {'form': form})


@login_required
def listar_agendamentos(request):
    data_param = request.GET.get('data')
    
    if data_param:
        try:
           data = datetime.datetime.strptime(data_param, "%Y-%m-%d").date()
        except ValueError:
            data = now().date()
    else:
        data = now().date() 

    agendamentos_list = Agendamento.objects.filter(data_agendamento=data).order_by('hora_agendamento')

   
    return render(request, 'agendamento/listar_agendamentos.html', {
        'agendamentos': agendamentos_list
    })

    
@login_required
def agendamentos_json(request):
    agendamentos = Agendamento.objects.all()
    eventos = []

    for ag in agendamentos:
        eventos.append({
            "title": ag.paciente.nome,
            "start": f"{ag.data_agendamento}T{ag.hora_agendamento}",
            "end": f"{ag.data_agendamento}T{ag.hora_agendamento}",
            "color": "red",            
        })

    return JsonResponse(eventos, safe=False)    


@login_required
def detalhes_paciente(request, pk):
    paciente = get_object_or_404(Contato, pk=pk)
    agendamentos = Agendamento.objects.filter(paciente=paciente).order_by('-data_agendamento', '-hora_agendamento')

    return render(request, 'agendamento/detalhes.html', {
        'paciente': paciente,
        'agendamentos': agendamentos,
    })


@require_POST
def editar_agendamento(request, agendamento_id):
    agendamento = get_object_or_404(Agendamento, id=agendamento_id)
    agendamento.status = request.POST.get('status')
    agendamento.observacao = request.POST.get('observacao')
    agendamento.save()
    
    return redirect('detalhes_paciente', agendamento.paciente.id)




@login_required
def medico_create(request):
    if request.method == "POST":
        nome = request.POST.get("nome", "").strip()
        crm = request.POST.get("crm", "").strip()
        uf_crm = request.POST.get("uf_crm", "").strip().upper()
        email = request.POST.get("email", "").strip() or None
        celular = request.POST.get("celular", "").strip() or None
        ativo = True if request.POST.get("ativo") == "on" else False
        especialidades_ids = request.POST.getlist("especialidades")

        if not especialidades_ids:
            messages.error(request, "Selecione pelo menos 1 especialidade.")
            return redirect("medico_create")

        try:
            medico = Medico.objects.create(
                nome=nome,
                crm=crm,
                uf_crm=uf_crm,
                email=email,
                celular=celular,
                ativo=ativo,
            )

            for esp_id in especialidades_ids:
                MedicoEspecialidade.objects.get_or_create(
                    medico=medico,
                    especialidade_id=esp_id,
                    defaults={"duracao_minutos": 30, "ativo": True}
                )

            messages.success(request, "Médico cadastrado com sucesso!")
            return redirect("medico_list")
            

        except Exception as e:
            messages.error(request, f"Erro ao cadastrar médico: {str(e)}")

    especialidades = Especialidade.objects.filter(ativo=True).order_by("nome")
    return render(request, "medico/medico_form.html", {"especialidades": especialidades})


@require_POST
@login_required
def especialidade_create_ajax(request):
    try:
        payload = json.loads(request.body.decode("utf-8"))
        nome = (payload.get("nome") or "").strip()

        if not nome:
            return JsonResponse({"error": "Nome é obrigatório."}, status=400)

        esp, created = Especialidade.objects.get_or_create(nome=nome, defaults={"ativo": True})
        if not created and not esp.ativo:
            esp.ativo = True
            esp.save()

        return JsonResponse({"id": esp.id, "nome": esp.nome}, status=201)

    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON inválido."}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    



def medico_create(request):
    if request.method == "POST":
        form = MedicoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Médico cadastrado com sucesso!")
            return redirect("medico_list")  # ajuste para sua url
        else:
            messages.error(request, "Preencha os campos corretamente.")
    else:
        form = MedicoForm()

    return render(request, "medico/medico_form.html", {"form": form})



# def medico_list(request):
#     q = (request.GET.get("q") or "").strip()

#     medicos = Medico.objects.all().order_by("nome")

#     if q:
#         medicos = medicos.filter(
#             Q(nome__icontains=q) |
#             Q(crm__icontains=q) |
#             Q(uf_crm__icontains=q) |
#             Q(email__icontains=q)
#         )

#     # para evitar N+1 quando pegar especialidades
#     medicos = medicos.prefetch_related("medicoespecialidade_set__especialidade")

#     return render(request, "medico/medico_list.html", {
#         "medicos": medicos,
#         "q": q,
#     })


def medico_list(request):
    q = (request.GET.get("q") or "").strip()
    page_number = request.GET.get("page", 1)

    qs = Medico.objects.all().order_by("nome").prefetch_related("medicoespecialidade_set__especialidade")

    if q:
        qs = qs.filter(
            Q(nome__icontains=q) |
            Q(crm__icontains=q) |
            Q(uf_crm__icontains=q) |
            Q(email__icontains=q)
        )

    paginator = Paginator(qs, 10)  # 10 por página (ajuste como quiser)
    page_obj = paginator.get_page(page_number)

    return render(request, "medico/medico_list.html", {
        "page_obj": page_obj,          #  objeto paginado
        "medicos": page_obj.object_list, # (opcional, pra você usar igual já usa)
        "q": q,
    })


@require_GET
def especialidades_por_medico(request):
    medico_id = request.GET.get("medico_id")
    if not medico_id:
        return JsonResponse({"especialidades": []})

    vinculos = (
        MedicoEspecialidade.objects
        .filter(medico_id=medico_id, ativo=True, especialidade__ativo=True)
        .select_related("especialidade")
        .order_by("-principal", "especialidade__nome")
    )

    return JsonResponse({
        "especialidades": [
            {"id": v.especialidade_id, "nome": v.especialidade.nome, "principal": v.principal}
            for v in vinculos
        ]
    })