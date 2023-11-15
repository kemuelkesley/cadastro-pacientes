from django.urls import path
from clinica.views import cadastro, sucesso, ClinicaListView ,ClinicaUpdateView


urlpatterns = [
   path('', ClinicaListView.as_view(), name='clinica_list'),
   path('update/<int:pk>/', ClinicaUpdateView.as_view(), name='clinica_update'),
   path('contato_form/', cadastro, name='contato_form'),
   path('sucesso/', sucesso, name='sucesso'),
]
