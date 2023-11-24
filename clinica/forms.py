from django import forms
from clinica.models import Contato
from django.core import validators
from phonenumber_field.formfields import PhoneNumberField
#from input_mask.widgets import InputMask



class ContatoForm(forms.ModelForm):

    nome = forms.CharField(        
        label='Nome', 
        max_length=50,
        required=True,   
        error_messages={"required": "Por favor entre com o seu nome"},
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite seu nome'}),          
    )
        
    email = forms.EmailField(
        label='Email', 
        max_length=50,
        required=True,  
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Insira seu email'}),            
    )    

    data_nascimento = forms.DateField(
        label='Data Nascimento', 
        required=True,   
        help_text='Formato: DD/MM/AAAA',
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),          
    )

    celular = PhoneNumberField(
        region='BR',
        label='Celular', 
        max_length=14, 
        required=True,   
        error_messages={"required": "Digite seu número de celular"},
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(82) 99999-9999'}),           
    )   



    class Meta:
        model = Contato
        fields = ['nome', 'email', 'data_nascimento', 'celular']
        
