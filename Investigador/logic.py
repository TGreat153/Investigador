import requests
from datetime import datetime
import json

def observar_data(data_inicial, data_final):
    if len(data_inicial) == 10 or len(data_final) == 10:
        dt_inicial = datetime.strptime(data_inicial, '%d/%m/%Y')
        dt_final = datetime.strptime(data_final, '%d/%m/%Y')
        diferenca = dt_final - dt_inicial
        return diferenca.days
    else:
        return 'Reprovou'

def formatar_data(data):
    lista = data.split('/')
    quant = len(lista)
    if quant == 3:
        data_oficial = lista[2] + lista[1] + lista[0]
        return data_oficial
    else:
        print('Error')

def criar_url(data_i, data_f):
    url_base = 'https://pncp.gov.br/api/consulta'
    endpoint = '/v1/contratos'
    url = url_base + endpoint + '?dataInicial=' + data_i + '&dataFinal=' + data_f + '&pagina='
    return url

def buscar_quant(url_base):
    pagina = 1
    url = url_base + str(pagina)
    r = requests.get(url)
    if r.status_code == 200:
        dados = r.json()
        return dados['totalPaginas']
    else:
        print("Erro ao acessar a API:", r.status_code)

def buscar_api(url, objeto, paginas):
    objeto = objeto.lower()
    lista_final = []
    u = 1
    i = 1
    while i <= paginas:
        if u < 2:
            url_final = url + str(i)
            r = requests.get(url_final)
            dados = json.loads(r.text)
            if objeto in str(dados['data']).lower():
                lista = dados['data']
                lista_filtrada = list(filter(lambda item: filtrar(objeto, item), lista))
                if len(lista_filtrada) > 0:
                    lista_final.append(lista_filtrada)
                    u = u + 1
            r.close()
            i = i + 1
        else:
            return lista_final
    return 'Não encontrado'

def filtrar(objeto, x):
    return objeto.lower() in str(x['objetoContrato']).lower()

def mostrar_dados(lista):
    print(lista)