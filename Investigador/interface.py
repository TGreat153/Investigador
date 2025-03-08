import ttkbootstrap as ttk
import logic

def ativar_data(entrada, msg):
    msg.pack_forget()
    return entrada.config(state='normal')

def mascara_data(evento, entrada, msg):
    valor = entrada.get()
    key = evento.keysym
    total = len(valor)
    if total < 9 or key == 'BackSpace':
        if key.isdigit() or key == 'BackSpace':
            if (total == 5 or total == 2) and key != 'BackSpace':
                entrada.insert(total,'/')
        else:
            msg.pack()
            return entrada.config(state='disable')
    elif total == 9:
        limitar_data(valor, entrada, msg)
    else:
        msg.pack()
        return entrada.config(state='disable')

def limitar_data(data, entrada, msg):
    lista = data.split('/')
    if int(lista[0]) > 31:
        msg.pack()
        return entrada.delete(0, ttk.END)
    if int(lista[1]) > 12:
        msg.pack()
        return entrada.delete(0, ttk.END)

def buscar(self, data_inicial, data_final, objeto):
    quant = buscar_base(data_inicial, data_final, objeto)
    if  quant != 'reprovou':
        return self.result(),
    else:
        ttk.dialogs.dialogs.Messagebox.ok('Digite um valor válido',title='Aviso')

def buscar_base(data_inicial, data_final, objeto):
    dt_incial = data_inicial.get()
    dt_final = data_final.get()
    diferenca = logic.observar_data(dt_incial, dt_final)
    if diferenca != 'Reprovou' and objeto.get():
        dt_i = logic.formatar_data(dt_incial)
        dt_f = logic.formatar_data(dt_final)
        url = logic.criar_url(dt_i, dt_f)
        return logic.buscar_quant(url)
    else:
        return 'reprovou'

def buscar_final(self, url, objeto, paginas):
    dados = logic.buscar_api(url, objeto, paginas)
    if dados != 'Não encontrado':
        return dados
    else:
        ttk.dialogs.dialogs.Messagebox.ok('Não encontrado', title='Aviso')
        self.home()

def colocar_valores(valor, lista_dados, lista_entrada):
    dados = int(valor) - 1
    filtro_lista = lista_dados[dados]
    if dados < 1:
        lista_entrada[0].delete(0, ttk.END)
        lista_entrada[1].delete(0,ttk.END)
        lista_entrada[2].delete(0, ttk.END)
        lista_entrada[3].delete(0, ttk.END)
        lista_entrada[4].delete(0, ttk.END)
        lista_entrada[5].delete(0, ttk.END)
        nome = filtro_lista[dados]['orgaoEntidade']['razaoSocial']
        cnpj = filtro_lista[dados]['orgaoEntidade']['cnpj']
        valor_inicial = filtro_lista[dados]['valorInicial']
        valor_global = filtro_lista[dados]['valorGlobal']
        codigo = filtro_lista[dados]['numeroControlePNCP']
        objeto = filtro_lista[dados]['objetoContrato']
        lista_entrada[0].insert(0, nome)
        lista_entrada[1].insert(0,cnpj)
        lista_entrada[2].insert(0, valor_inicial)
        lista_entrada[3].insert(0, valor_global)
        lista_entrada[4].insert(0, codigo)
        lista_entrada[5].insert(0, objeto)


class App:
    def __init__(self, master):
        self.frame = ttk.Frame(master)
        self.frame.pack()
        self.nome = ttk.Label(self.frame, text='Investigador', font=('',21))
        self.nome.pack()
        self.home()
    def home(self):
        self.frame_principal = ttk.Frame(self.frame)
        self.frame_principal.pack()
        self.dt  = ttk.Frame(self.frame_principal)
        self.dt.pack(pady=25)
        self.msg = ttk.Label(text='Digite uma data válida')
        self.dt_inicial_txt = ttk.Label(self.dt,text='De: ')
        self.dt_inicial_txt.pack(side='left')
        self.dt_inicial = ttk.Entry(self.dt,width=10)
        self.dt_inicial.pack(side='left')
        self.dt_inicial.bind('<Key>',lambda evento, entrada = self.dt_inicial, msg = self.msg: mascara_data(evento, entrada, msg))
        self.dt_inicial.bind('<ButtonPress>', lambda evento, entrada=self.dt_inicial, msg = self.msg: ativar_data(entrada,msg))
        self.dt_final_txt = ttk.Label(self.dt,text='Até: ')
        self.dt_final_txt.pack(side='left', padx=(10,0))
        self.dt_final = ttk.Entry(self.dt,width=10) #Data Final
        self.dt_final.pack(side='left')
        self.dt_final.bind('<Key>',lambda evento, entrada = self.dt_final, msg = self.msg: mascara_data(evento, entrada, msg))
        self.dt_final.bind('<ButtonPress>', lambda evento, entrada=self.dt_final, msg = self.msg: ativar_data(entrada,msg))
        self.obj = ttk.Frame(self.frame_principal)
        self.obj.pack()
        self.objeto_text = ttk.Label(self.obj, text='Digite o objeto:')
        self.objeto_text.pack(side='left', padx=(10,0), pady=(0,20))
        self.objeto = ttk.Entry(self.obj)
        self.objeto.pack(side='left', pady=(0,20))
        self.buscar_b1 = ttk.Button(self.frame_principal, text='Buscar', bootstyle='success', command= lambda data_inicial = self.dt_inicial, data_final = self.dt_final, objeto = self.objeto: buscar(self, data_inicial, data_final, objeto))
        self.buscar_b1.pack(fill='x')
    def result(self):
        self.msg.destroy()
        data_inicial = logic.formatar_data(self.dt_inicial.get())
        data_final = logic.formatar_data(self.dt_final.get())
        objeto = self.objeto.get()
        for i in self.frame_principal.winfo_children():
            i.destroy()
        url = logic.criar_url(data_inicial, data_final)
        paginas = logic.buscar_quant(url)
        self.lista_dados = buscar_final(self,url, objeto, paginas)
        self.frame_principal = ttk.Frame(self.frame)
        self.frame_principal.pack(side='left')
        #Lista suspensa
        self.lista_suspensa = ttk.Frame(self.frame_principal).pack()
        self.escolha_text = ttk.Label(self.lista_suspensa,text='Escolha o numero do contrato: ')
        self.escolha_text.pack()
        valores = [1, 2, 3, 4, 5]
        padrao = ttk.StringVar()
        padrao.set(valores[0])
        self.escolha = ttk.OptionMenu(self.lista_suspensa, padrao, *valores, bootstyle='light').pack()
        #Valores
        self.Name = ttk.Frame(self.frame_principal).pack()
        self.Name_text = ttk.Label(self.Name,text='Nome: ').pack()
        self.Name_valor = ttk.Entry(self.Name)
        self.Name_valor.pack()
        self.cnpj = ttk.Frame(self.frame_principal).pack()
        self.cnpj_text = ttk.Label(self.cnpj,text='CNPJ: ').pack()
        self.cnpj_valor = ttk.Entry(self.cnpj)
        self.cnpj_valor.pack()
        self.valor_inicial = ttk.Frame(self.frame_principal).pack()
        self.valor_inicial_text = ttk.Label(self.valor_inicial,text='Valor Inicial: ').pack()
        self.valor_inicial_valor = ttk.Entry(self.valor_inicial)
        self.valor_inicial_valor.pack()
        self.valor_global = ttk.Frame(self.frame_principal).pack()
        self.valor_global_text = ttk.Label(self.valor_global,text='Valor global: ').pack()
        self.valor_global_valor = ttk.Entry(self.valor_global)
        self.valor_global_valor.pack()
        self.codigo = ttk.Frame(self.frame_principal).pack()
        self.codigo_text = ttk.Label(self.codigo, text='Codigo: ').pack()
        self.codigo_valor = ttk.Entry(self.codigo)
        self.codigo_valor.pack()
        self.objeto = ttk.Frame(self.frame_principal).pack()
        self.objeto_text = ttk.Label(self.objeto, text='Objeto do contrato: ').pack()
        self.objeto_valor = ttk.Entry(self.objeto)
        self.objeto_valor.pack()
        self.button_submit = ttk.Button(self.lista_suspensa, text='Colocar', bootstyle='success',command=lambda lista_dados = self.lista_dados, valor=padrao.get(),lista_entrada=[self.Name_valor, self.cnpj_valor,self.valor_inicial_valor, self.valor_global_valor,self.codigo_valor,self.objeto_valor]: colocar_valores(valor,lista_dados,lista_entrada)).pack(pady=(20, 20))