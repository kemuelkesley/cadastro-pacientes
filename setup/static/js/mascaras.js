// ativar campo data de nascimento e celular
$(document).ready(function(){
    $('#id_data_nascimento').mask('00/00/0000');
    $('#id_celular').mask('(00) 00000-0000');    
    $('#id_cpf').mask('000.000.000-00');
    $('#id_cep').mask('00000-000');
    $('#id_uf').mask('AA');
});


