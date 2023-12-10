from django import forms
import datetime

def validate_nome(value):
    if len(value) <= 2:
        raise forms.ValidationError("Nome deve ter mais de 2 caracteres")
    if any(char.isdigit() for char in value):
        raise forms.ValidationError("Nome não pode conter números")
    
    return value
    

def validate_celular(value):
    if len(value) < 14:
        raise forms.ValidationError("Celular deve ter 11 digitos")
        
    return value    
 
    

def validate_data_nascimento(value):    
    if value > datetime.date.today():
        raise forms.ValidationError("Data de nascimento inválida")
    elif value < datetime.date(1900, 1, 1):
        raise forms.ValidationError("Ano de nascimento inválido")
   
    validate_idade(value)


    return value


def validate_idade(data_nascimento):
    hoje = datetime.date.today()
    idade = hoje.year - data_nascimento.year - ((hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day))

    if idade < 18:
        raise forms.ValidationError("Você deve ser maior de 18 anos para se cadastrar.")


