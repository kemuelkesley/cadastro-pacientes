from django import forms
import datetime
import re

# Tentar usar biblioteca externa `validate-docbr` quando disponível (melhor validação de CPF)
try:
    from validate_docbr import CPF as _CPFValidator
except Exception:
    _CPFValidator = None

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
    return idade
    # if idade < 18:
    #     raise forms.ValidationError("Você deve ser maior de 18 anos para se cadastrar.")

def validate_cpf(value):
    """Valida CPF no formato 000.000.000-00 ou somente dígitos.
    Remove não-dígitos e valida usando o algoritmo oficial.
    """
    if not value:
        raise forms.ValidationError("CPF é obrigatório")

    # Se a biblioteca validate-docbr estiver disponível, utilize-a (mais robusta)
    if _CPFValidator is not None:
        cpf_validator = _CPFValidator()
        if not cpf_validator.validate(value):
            raise forms.ValidationError("CPF inválido")
        return value

    # Remove tudo que não for dígito
    digits = re.sub(r"\D", "", value)

    if len(digits) != 11:
        raise forms.ValidationError("CPF inválido")

    # Rejeita CPFs com todos os dígitos iguais (ex.: 11111111111)
    if digits == digits[0] * 11:
        raise forms.ValidationError("CPF inválido")

    def calc_dv(digs):
        s = sum((int(d) * w) for d, w in zip(digs, range(len(digs)+1, 1, -1)))
        r = (s * 10) % 11
        return r if r < 10 else 0

    dv1 = calc_dv(digits[:9])
    dv2 = calc_dv(digits[:10])

    if dv1 != int(digits[9]) or dv2 != int(digits[10]):
        raise forms.ValidationError("CPF inválido")

    return value

