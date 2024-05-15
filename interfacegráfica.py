import customtkinter as ct
from CTkMenuBar import *
import sqlite3
from datetime import datetime
import pandas as pd

def dataMaxima(tbl, banco = 'djo.sqlite3'):
    banco = sqlite3.connect(banco)
    cursor = banco.cursor()
    cursor.execute(f"""SELECT MAX(DATA_MOVIMENTO) FROM '{tbl}'""")
    data = cursor.fetchall()[0][0]
    return data

def retPorData(tbl, data, banco = 'djo.sqlite3'):
    banco = sqlite3.connect(banco)
    cursor = banco.cursor()
    dataTempo = data + " 00:00"
    dataTempo = datetime.strptime(dataTempo, '%d/%m/%Y %H:%M')
    cursor.execute(f"""SELECT * FROM '{tbl}'
                    WHERE DATA_MOVIMENTO = '{dataTempo}'""")
    colunas = ['NUMERO_DO_PROCESSO', 'NOME_DO_TRIBUNAL', 'NOME_DA_COMARCA',  'ORGAO',  'DEPENDENCIA',
                                   'NOME_RECLAMANTE',  'CPF_CNPJ_RECLAMANTE',
                                   'NOME_RECLAMADO',  'CPF_CNPJ_RECLAMADO',
                                  'CONTA_JUDICIAL',  'PARCELA',
                                   'NUMERO_DA_GUIA',  'DATA_DO_DEPOSITO',
                                   'VALOR_SALDO_CAPITAL',  'VALOR_CORRECAO_MONETARIA',
                                   'VALOR_JUROS',  'VALOR_SALDO_CORRIGIDO',
                                   'VALOR_IR',  'DATA_PROCESSAMENTO',
                                   'CD_PRD_BNC',  'NR_SEQUENCIAL_LEGISLACAO_TRIBUTARIA',  'NUMERO_LEI_TRIBUTARIA',
                                   'DATA_MOVIMENTO',  'ARQUIVO', 'TIPO_ARQUIVO']
    df = pd.DataFrame(cursor.fetchall(), columns=colunas)
    print(df.head())
    return df

class App(ct.CTk):
    def __init__(self):
        super().__init__()
        self.title("SADJud")
        w = 1024
        h = 760
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        x = (ws/2)-(w/2)
        y = (hs/2)-(h/2)
        self.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.menu = self.menus()

    def menus(self):
        menu = CTkMenuBar(self)
        btnResFavGov = menu.add_cascade("Resgates a Favor do Estado")
        dropdown1 = CustomDropdownMenu(widget=btnResFavGov)
        dropdown1.add_option(option="Por Data", command=self.rfvPorData)
        dropdown1.add_separator()
        dropdown1.add_option(option="Por Conta Judicial")
        dropdown1.add_separator()
        dropdown1.add_option(option="Por Processo Judicial")
        dropdown1.add_separator()
        dropdown1.add_option(option="Por CPF/CNPJ do Reclamante")
        dropdown1.add_separator()
        dropdown1.add_option(option="Por CPF/CNPJ do Reclamado")
        dropdown1.add_separator()
        dropdown1.add_option(option="Por CPF/CNPJ do Reclamante")
        dropdown1.add_separator()
        dropdown1.add_option(option="Por Nome do Reclamante")
        dropdown1.add_separator()
        dropdown1.add_option(option="Por Nome do Reclamado")
        dropdown1.add_separator()
        btnSair = menu.add_cascade("Sair")
        dropdownsair = CustomDropdownMenu(widget=btnSair)
        dropdownsair.add_option(option="Sobre")
        dropdownsair.add_separator()
        dropdownsair.add_option(option="Sair", command=quit)

    def rfvPorData(self):
        rfvDataWindow  = ct.CTkToplevel(self)
        rfvDataWindow.title("Resgates a Favor do Governo por Data")
        w = 400
        h = 200
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        rfvDataWindow.geometry('%dx%d+%d+%d' % (w, h, x, y))
        rfvDataWindow.resizable(False, False)
        label = ct.CTkLabel(rfvDataWindow, text='Data')
        label.place(x = 110, y = 70)
        dataInfo = ct.CTkEntry(rfvDataWindow, placeholder_text='dd/mm/yyyy')
        dataInfo.place(x = 150, y = 70)
        def pesquisarPorData():
            retPorData(tbl = 'resgatesafavordogoverno', data=dataInfo.get())
            fecharJanela()
        def fecharJanela():
            rfvDataWindow.destroy()
            rfvDataWindow.update()
        btnExecutar = ct.CTkButton(rfvDataWindow, text='Pesquisar', command=pesquisarPorData)
        btnExecutar.place(x = 130, y = 110)













app = App()
app.mainloop()