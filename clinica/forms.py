from django import forms
from clinica.models import Contato


class ContatoForm(forms.ModelForm):

    nome = forms.CharField(
        label='Nome', 
        max_length=50,
        required=True,   
        widget=forms.TextInput(attrs={'class': 'form-control'}),           
    )
        
    email = forms.EmailField(
        label='Email', 
        max_length=50,
        required=True,  
        widget=forms.TextInput(attrs={'class': 'form-control'}),            
    )       

    class Meta:
        model = Contato
        fields = ['nome', 'email']
        
       

        

