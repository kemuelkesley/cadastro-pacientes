from django import forms
from clinica.models import Contato, Agendamento
from django.core import validators
from phonenumber_field.formfields import PhoneNumberField
from .validators import validate_nome, validate_celular, validate_data_nascimento
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class ContatoForm(forms.ModelForm):

    nome = forms.CharField(        
        label='Nome', 
        max_length=50,
        required=True,   
        validators=[validate_nome],
        widget=forms.TextInput(attrs={
            'class': 'form-control custom-input', 
            'placeholder': 'Digite seu nome',
        }),          
    )
        
    email = forms.EmailField(
        label='E-mail', 
        max_length=50,
        required=True,  
        widget=forms.TextInput(attrs={'class': 'form-control custom-input', 'placeholder': 'Insira seu email'}),            
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
   

    class Meta:
        model = Contato
        fields = ['nome', 'email', 'data_nascimento', 'celular']
 



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

    # def __init__(self, *args, **kwargs):
    #     super(CadastroForm, self).__init__(*args, **kwargs)
    #     self.fields['username'].widget.attrs.update({'class': 'form-control'})
    #     self.fields['password1'].widget.attrs.update({'class': 'form-control'})
    #     self.fields['password2'].widget.attrs.update({'class': 'form-control'})


class AgendamentoForm(forms.ModelForm):
    class Meta:
        model = Agendamento
        fields = ['paciente', 'data_agendamento', 'hora_agendamento', 'observacao']
        widgets = {
            'data_agendamento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'hora_agendamento': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'paciente': forms.Select(attrs={'class': 'form-control'}),
            'observacao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        data = cleaned_data.get('data_agendamento')
        hora = cleaned_data.get('hora_agendamento')

        if data and hora:
            conflito = Agendamento.objects.filter(
                data_agendamento=data,
                hora_agendamento=hora
            )

            # Ignora o próprio agendamento ao editar
            if self.instance.pk:
                conflito = conflito.exclude(pk=self.instance.pk)

            if conflito.exists():
                raise forms.ValidationError("Já existe um agendamento para essa data e hora.")

        return cleaned_data