from django.shortcuts import render

# Create your views here.
def contratos(request):
    return render(request,'contratos/contratos.html')

def cadastros(request):
    return render(request, 'cadastros/cadastros.html')

def editar(request):
    return render(request, 'editar/editar.html')

def visualizar(request):
    return render(request, 'visualizar/visualizar.html')