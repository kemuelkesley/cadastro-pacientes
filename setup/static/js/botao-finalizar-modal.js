$(document).ready(function(){
    // Alteração aqui: usamos uma classe para acionar o evento click
    $('.finalizar-botao').click(function() {
        $('#confirmModal').modal('show');
    });

    $('#confirmarBotao').click(function() {
        // Aqui você pode adicionar a lógica para salvar as alterações (enviar o formulário) e redirecionar
        $('form').submit();
        $('#confirmModal').modal('hide');
    });
});
