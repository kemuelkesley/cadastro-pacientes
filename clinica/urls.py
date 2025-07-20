from django.urls import path
from clinica.views import cadastro, sucesso, deletar_contato, ClinicaListView ,ClinicaUpdateView, cadastrar_usuario, index, login, deslogar_usuario,logar_usuario, agendar_consulta, listar_agendamentos


urlpatterns = [
   path('logar_usuario/', logar_usuario, name="logar_usuario"),
   path('cadastrar_usuario/', cadastrar_usuario, name="cadastrar_usuario"),
   path('deslogar_usuario/', deslogar_usuario, name="deslogar_usuario"),
   path('index/', index, name="index"),
   path('clinica_list/', ClinicaListView.as_view(), name='clinica_list'),
   path('clinica_update/<int:pk>/', ClinicaUpdateView.as_view(), name='clinica_update'),
   path('deletar_contato/<int:pk>/', deletar_contato, name='deletar_contato'),
   path('contato_form/', cadastro, name='contato_form'),
   path('sucesso/', sucesso, name='sucesso'),
   path('agendar_consulta/', agendar_consulta, name='agendar_consulta'),
   path('listar_agendamentos/', listar_agendamentos, name='listar_agendamentos')
]
