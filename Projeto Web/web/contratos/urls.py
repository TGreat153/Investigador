from django.urls import path

from . import views

urlpatterns = [
    path("", views.contratos, name="contratos"),
    path("cadastros",views.cadastros, name="cadastros"),
    path("editar",views.editar, name="editar"),
    path("visualizar",views.visualizar, name="visualizar")
]