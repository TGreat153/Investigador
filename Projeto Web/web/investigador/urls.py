from django.urls import path

from . import views

urlpatterns = [
    path("", views.investigador, name="investigador"),
    path("/resultados/<str:data_inicial>/<str:data_final>/<str:objeto>/", views.resultados, name='resultados'),
    #path("/resultados/<str:data_inicial>/<str:data_final>/<str:objeto>/", views.resultados_rep, name='resultados_rep')
]
