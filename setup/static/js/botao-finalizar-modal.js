
$(document).ready(function(){    
    $('.finalizar-botao').click(function() {
        $('#confirmModal').modal('show');
    });

    $('#confirmarBotao').click(function() {       
        $('form').submit();
        $('#confirmModal').modal('hide');
    });
});
