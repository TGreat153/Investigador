from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import nr_cont_Form
# Create your views here.
def contratos(request):
    return render(request,'contratos/contratos.html')

def cadastros(request):
    if request.method == 'POST':
        form = nr_cont_Form(request.POST)
        if form.is_valid():
            print(type(form))
            #form.save()
        else:
            print(form.errors)
            form = nr_cont_Form
            return render(request, 'cadastros\cadastros.html', {'form': form})
    return render(request, 'cadastros\cadastros.html')



def editar(request):
    return render(request, 'editar/editar.html')

def visualizar(request):
    return render(request, 'visualizar/visualizar.html')

#Lógica

def pegar_objetos(request, lista):
    lista_final = []
    print(lista[1])
    for valor in range(len(lista)):
        valor_final = request.POST.get(valor, 'Não encontrado')
        lista_final.append(valor_final)
    return lista_final