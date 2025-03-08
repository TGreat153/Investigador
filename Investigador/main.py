from ttkbootstrap.constants import *
import ttkbootstrap as ttk
import interface

#Base da janela
janela = ttk.Window(themename='simplex')
janela.geometry('800x800')
janela.title('Investigador')
janela.iconbitmap('Investigador.ico')

#Rodar Janela
interface.App(janela)
janela.mainloop()