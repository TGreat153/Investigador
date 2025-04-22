import requests, json
from django.shortcuts import render, redirect
from django.contrib import messages
import time

app_name = 'investigador'

# Create your views here.
def investigador(request):
    data_inicial = ''
    data_final = ''
    objeto = ''
    if request.method == 'GET':
        data_inicial = request.GET.get('dt_inicial')
        data_final = request.GET.get('dt_final')
        objeto = request.GET.get('objeto')
        if data_inicial == '' and data_final == '' and objeto == '':
         messages.add_message(request, messages.ERROR, "Valores incompletos!")
         return render(request,'investigador/invest.html')
        if data_inicial ==  None or data_final == None or objeto == None:
           return render(request,'investigador/invest.html')
        else:
           return redirect('resultados',data_inicial=data_inicial, data_final=data_final, objeto=objeto)
        
def resultados(request, data_inicial, data_final, objeto):
   def filtrar(x):
     return objeto.lower() in str(x['objetoContrato']).lower()
   dt_i = converterData(data_inicial)
   dt_f = converterData(data_final)
   url = colocar_base(dt_i, dt_f)
   total = buscar_quant(url)
   total_final = buscar_inicial(objeto, total, url, filtrar)
   return render(request, "investigador/resultados.html", {"itens": total_final})



'''def resultados_rep(request, data_inicial, data_final, objeto, i):
   def filtrar(x):
     return objeto.lower() in str(x['objetoContrato']).lower()
   dt_i = converterData(data_inicial)
   dt_f = converterData(data_final)
   url = colocar_base(dt_i, dt_f)
   total = buscar_quant(url)
   total_final = buscar_rep(objeto, total, url, filtrar, i)
   return render(request, "investigador/resultados.html", {"itens": total_final})
'''
   
#Utilidades
    
def converterData(data):
  lista = data.split('-')
  quant = len(lista)
  if quant == 3:
    data_certa = lista[0] + lista[1] + lista[2]
    return data_certa
  
def colocar_base(data_inicial, data_final):
   url_base = 'https://pncp.gov.br/api/consulta'
   endpoint = '/v1/contratos'
   return url_base + endpoint + '?dataInicial=' + data_inicial + '&dataFinal=' +  data_final + '&pagina='

def buscar_quant(url):
  pagina = 1
  url_final = url + str(pagina)
  r = requests.get(url_final)
  if r.status_code == 200:
    dados = r.json()
    return dados['totalPaginas']
  else:
     return 'error'
  
def buscar_dados(url, total, objeto):
  def filtrar(x):
   return objeto.lower() in str(x['objetoContrato']).lower()
  objeto = objeto.lower()
  i = 0
  i = i + 1
  resultado = ''
  while i <= total :
    url_final = url + str(i)
    r = requests.get(url_final)
    dados = json.loads(r.text)
    if objeto in str(dados['data']).lower():
      resultado = dados['data']
      lista_filtrada = list(filter(filtrar, resultado))
      if len(lista_filtrada) > 0:
        result_final = mostrar_dados(lista_filtrada)
    r.close()
    i = 1 + i
  print('Não encontrado')

def mostrar_dados(lista, i):
  if len(lista) > 0:
    dados = lista[0]
    cnpj = dados['orgaoEntidade']['cnpj']
    nome_empresa = dados['orgaoEntidade']['razaoSocial']
    valor_inicial = dados['valorInicial']
    valor_global = dados['valorGlobal']
    objeto_contrato = dados['objetoContrato']
    data_assinatura = dados['dataAssinatura']
    codigo = dados['numeroControlePNCP']
    quantas_vezes = i
    lista_final = [cnpj, nome_empresa, valor_inicial, valor_global, objeto_contrato, data_assinatura, codigo, quantas_vezes]
    return lista_final
  
def mudar_pagina(request):
  render(request, "investigador/resultados.html")


def buscar_inicial(objeto, total, url, filtrar):
  objeto = objeto.lower()
  i = 0
  i = i + 1
  resultado = ''
  while i <= total:
      url_final = url + str(i)
      r = requests.get(url_final)
      dados = json.loads(r.text)
      if objeto in str(dados['data']).lower():
         resultado = dados['data']
         lista_filtrada = list(filter(filtrar, resultado))
         if len(lista_filtrada) > 0:
            result_final = mostrar_dados(lista_filtrada, i)
            return result_final
      r.close()
      i = 1 + i
      if i % 20 == 0:
        time.sleep(10)


'''def buscar_rep(objeto, total, url, filtrar, i, itens):
  objeto = objeto.lower()
  resultado = ''
  while i <= total:
      url_final = url + str(i)
      r = requests.get(url_final)
      dados = json.loads(r.text)
      if objeto in str(dados['data']).lower():
         resultado = dados['data']
         lista_filtrada = list(filter(filtrar, resultado))
         if len(lista_filtrada) > 0:
            result_final = mostrar_dados(lista_filtrada, itens[-1])
            return result_final
      r.close()
      i = 1 + i
      if i % 20 == 0:
        time.sleep(10)'''