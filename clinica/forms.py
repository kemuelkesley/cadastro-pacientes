import time
from django import forms
from clinica.models import Contato, Agendamento, Especialidade, Medico, MedicoEspecialidade
from django.core import validators
from phonenumber_field.formfields import PhoneNumberField
from .validators import validate_nome, validate_celular, validate_data_nascimento, validate_cpf
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from datetime import datetime, date, time


class ContatoForm(forms.ModelForm):

    nome = forms.CharField(        
        label='Nome', 
        max_length=50,
        required=True,   
        validators=[validate_nome],
        widget=forms.TextInput(attrs={
            'class': 'form-control custom-input', 
            'placeholder': 'Nome completo',
        }),          
    )
        
    email = forms.EmailField(
        label='E-mail', 
        max_length=50,
        required=True,  
        widget=forms.TextInput(attrs={'class': 'form-control custom-input', 'placeholder': 'email@exemplo.com'}),            
    )    

    cpf = forms.CharField(
        label='CPF',
        max_length=14,
        required=True,
        validators=[validate_cpf],        
        widget=forms.TextInput(attrs={
            'class': 'form-control custom-input', 
            'placeholder': '000.000.000-00', 
            'data-mask': '000.000.000-00', 
            'id': 'id_cpf'
        }),
    )


    data_nascimento = forms.DateField(
        label='Data de Nascimento', 
        required=True, 
        validators=[validate_data_nascimento], 
        widget=forms.DateInput(attrs={
            'class': 'form-control custom-input',
            'type' : 'data',
            'data-mask' : "00/00/0000",
            'placeholder' : 'dd/mm/aaaa'
        }), 
    )



    celular = forms.CharField(
        label='Celular', 
        max_length=15, 
        required=True,
        validators=[validate_celular],   
        widget=forms.TextInput(attrs={
            'class': 'form-control custom-input',
            'data-mask':"(00) 00000-0000", 
            'placeholder': '(00) 0000-0000'
        }),
    )

    rua = forms.CharField(
        label='Rua',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control custom-input',
            'placeholder': 'Nome da rua',
        }),
    )

    numero = forms.CharField(
        label ='Número',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control custom-input', 
            'placeholder': '123',
        })
    )

    bairro = forms.CharField(
        label='Bairro',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control custom-input',
            'placeholder': 'Nome do bairro',
        }),
    )
    

    cep = forms.CharField(
        label='CEP',
        max_length=9,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control custom-input',
            'data-mask':"00000-000",
            'placeholder': '00000-000'
        }),
    )

    estado = forms.CharField(
        label='Estado',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control custom-input',
            'placeholder': 'Estado',
        }),
    )

    uf = forms.CharField(
        label='UF',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control custom-input',
            'placeholder': 'UF',
        }),
    )


    class Meta:
        model = Contato
        fields = [
            'nome',
            'email', 
            'cpf', 
            'data_nascimento', 
            'celular', 
            'cep', 
            'rua', 
            'numero', 
            'bairro', 
            'estado', 
            'uf'
        ]



class CadastroForm(UserCreationForm):

    username = forms.CharField(
        label='Usuário', 
        max_length=50,
        required=True,           
        widget=forms.TextInput(attrs={
            'class': 'form-control custom-input', 
            'placeholder': 'Crie um nome de usuário',
        }),          
    )

    password1 = forms.CharField(
        label='Senha', 
        max_length=50,
        required=True,  
        widget=forms.PasswordInput(attrs={
            'class': 'form-control custom-input',
            'placeholder': 'Insira sua senha'
        }),              
    )

    password2 = forms.CharField(
        label='Confirmar Senha', 
        max_length=50,
        required=True,  
        widget=forms.PasswordInput(attrs={
            'class': 'form-control custom-input',
            'placeholder': 'Confirme sua senha'
        }),              
    )


    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']



# Função para gerar opções de horário
def gerar_horarios():
    return [time(h, m).strftime("%H:%M") for h in range(7, 17) for m in (0, 30)] + ['17:00']

class AgendamentoForm(forms.ModelForm):
    hora_agendamento = forms.ChoiceField(choices=[], label="Hora")

    class Meta:
        model = Agendamento
        fields = ['paciente', 'data_agendamento', 'hora_agendamento', 'observacao']
        widgets = {
            'data_agendamento': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control custom-input', 'placeholder': 'Selecione a data',
                'id': 'id_data_agendamento',
                'min': datetime.today().strftime('%Y-%m-%d'),
            }),
            'paciente': forms.Select(attrs={'class': 'form-control custom-input'}),
            'observacao': forms.Textarea(attrs={'class': 'form-control custom-input', 'placeholder': 'Insira observações', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        data = None
        if self.data.get('data_agendamento'):
            try:
                data = datetime.strptime(self.data.get('data_agendamento'), "%Y-%m-%d").date()
            except ValueError:
                pass

        horarios_disponiveis = gerar_horarios()

        if data:
            horarios_ocupados = Agendamento.objects.filter(data_agendamento=data).values_list('hora_agendamento', flat=True)
            horarios_ocupados = [hora.strftime("%H:%M") for hora in horarios_ocupados]
            horarios_disponiveis = [h for h in horarios_disponiveis if h not in horarios_ocupados]

        self.fields['hora_agendamento'].choices = [(h, h) for h in horarios_disponiveis]
        self.fields['hora_agendamento'].widget.attrs.update({'class': 'form-control custom-input'})

    def clean(self):
        cleaned_data = super().clean()
        data = cleaned_data.get('data_agendamento')
        hora_str = cleaned_data.get('hora_agendamento')

        if data and hora_str:
            hora = time.fromisoformat(hora_str)

            if data == date.today() and hora <= datetime.now().time():
                raise forms.ValidationError("Você não pode agendar para um horário que já passou hoje.")

        return cleaned_data    
    




class MedicoForm(forms.ModelForm):
    # Campo EXTRA (não existe no model Medico diretamente)
    # (porque especialidades é M2M com through, então não dá pra usar direto)
    especialidades = forms.ModelMultipleChoiceField(
        queryset=Especialidade.objects.filter(ativo=True).order_by("nome"),
        widget=forms.SelectMultiple(attrs={"class": "form-select custom-input", "multiple": "multiple"}),
        required=True,
        label="Especialidades",
    )

    class Meta:
        model = Medico
        fields = ["nome", "crm", "uf_crm", "email", "celular", "ativo"]  # campos do seu HTML
        widgets = {
            "nome": forms.TextInput(attrs={"class": "form-control custom-input", "placeholder": "Ex: Dra. Maria Souza"}),
            "crm": forms.TextInput(attrs={"class": "form-control custom-input", "placeholder": "Ex: 12345"}),
            "uf_crm": forms.TextInput(attrs={"class": "form-control custom-input", "placeholder": "SP", "maxlength": "2"}),
            "email": forms.EmailInput(attrs={"class": "form-control custom-input", "placeholder": "medico@clinica.com"}),
            "celular": forms.TextInput(attrs={"class": "form-control custom-input", "placeholder": "(xx) xxxxx-xxxx"}),
        }
        labels = {
            "nome": "Nome do Médico",
            "uf_crm": "UF CRM",
            "celular": "Celular",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Se estiver editando, marcar especialidades atuais como selecionadas
        if self.instance and self.instance.pk:
            atuais = Especialidade.objects.filter(
                medicoespecialidade__medico=self.instance,
                medicoespecialidade__ativo=True,
            ).distinct()
            self.fields["especialidades"].initial = atuais

    def clean_uf_crm(self):
        uf = (self.cleaned_data.get("uf_crm") or "").strip().upper()
        if len(uf) != 2:
            raise forms.ValidationError("UF deve ter 2 caracteres (ex: SP).")
        return uf

    def save(self, commit=True):
        medico = super().save(commit=commit)

        # Atualiza os vínculos (through)
        especialidades_selecionadas = self.cleaned_data.get("especialidades")

        if commit:
            # marca todas como inativas primeiro (soft delete do vínculo)
            MedicoEspecialidade.objects.filter(medico=medico).update(ativo=False)

            # reativa/cria as selecionadas
            for esp in especialidades_selecionadas:
                MedicoEspecialidade.objects.update_or_create(
                    medico=medico,
                    especialidade=esp,
                    defaults={"ativo": True},
                )

        return medico