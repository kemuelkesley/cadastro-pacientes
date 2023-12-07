from django import forms

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
 
    
    



