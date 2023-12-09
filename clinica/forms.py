from django import forms
from clinica.models import Contato
from django.core import validators
from phonenumber_field.formfields import PhoneNumberField
from .validators import validate_nome, validate_celular, validate_data_nascimento





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
        label='Email', 
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


   
