# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.db.models import Q
# from django.views.generic import ListView
# from django.core.paginator import Paginator
# from clinica.models import Contato




# def buscar_contatos(nome):
#     if nome:
#         return Contato.objects.filter(
#             Q(nome__icontains=nome) | Q(email__icontains=nome)
#         )

#     else:
#         return Contato.objects.all()


# def criar_paginacao(request, objeto):
#     paginator = Paginator(objeto, 10)
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)

#     return page_obj


# class ClinicaListView(LoginRequiredMixin,ListView):
#     model = Contato
#     template_name = "clinica/clinica_list.html"
#     context_object_name = "clinica_list"

#     def get_queryset(self):
#         nome = self.request.GET.get("nome", None)
#         return buscar_contatos(nome).filter(ativo=True)
#         # return buscar_contatos(nome)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         objeto = self.get_queryset()
#         page_obj = criar_paginacao(self.request, objeto)
#         context["page_obj"] = page_obj
#         context["criar_paginacao"] = criar_paginacao(
#             self.request, Contato.objects.all()
#         )  # Use uma consulta diferente para a paginação

#         return context
