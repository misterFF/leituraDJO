import customtkinter as ct
from CTkMenuBar import *
from datetime import datetime
import pandas as pd
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox 
import os
import re

def origem():
    directory = filedialog.askdirectory()
    lblOrigem.config(text = directory)
def destino():
    directory = filedialog.askdirectory()
    lblDestino.config(text = directory)
def leitura_arquivo():
    import pandas as pd
    import logging    
    log = lblDestino.cget("text")+'/'+"log.txt"    
    logging.basicConfig(level=logging.INFO, filename=log, format="%(asctime)s - %(levelname)s - %(message)s")
    arqsSucesso = []
    arqsFalha = []
    largurasColunasTipoA = [1, 25, 25, 25, 25, 4, 30, 14, 30, 14, 257]
    arquivos = os.listdir(lblOrigem.cget("text"))
    arquivos = [arq for arq in arquivos if "djo190" in arq]
    for arq in arquivos:
        caminhoTotal = lblOrigem.cget("text")+'/'+arq
        print(f'Processando o arquivo {caminhoTotal}')
        baseLidaA = pd.read_fwf(caminhoTotal, header=None, widths=largurasColunasTipoA, encoding='unicode_escape')    
        tipoArquivo = baseLidaA.loc[5, 1]

        if tipoArquivo == "RESUMO DO MOVIMENTO DIARI":

            largurasColunasTipoA = [37, 22, 27, 27]
            baseLidaA = pd.read_fwf(caminhoTotal, header=None, widths=largurasColunasTipoA, encoding='unicode_escape')
            dataArquivo = baseLidaA.loc[3, 0][-10:].replace(".", "_")
            nomeArquivo = f"{tipoArquivo} {dataArquivo}.xlsx"           

            baseLidaA = baseLidaA.drop(range(6))
            baseLidaA.iloc[0][0] = "Data"
            baseLidaA.iloc[0][1] = dataArquivo            

            for i in range(len(baseLidaA)):

                check = re.search(r"(\W*\d*\W*\d*\W*\d*\W*\d*\W*\d*\W*\d*)(-$)", str(baseLidaA.iloc[i][1]))
                if check:
                    baseLidaA.iloc[i][1] = check.group(2) + check.group(1)
                if not(pd.isnull(baseLidaA.iloc[i][1]) or baseLidaA.iloc[i][1] == "CAPITAL"):
                    baseLidaA.iloc[i][1] = baseLidaA.iloc[i][1].replace(".", "")
                    baseLidaA.iloc[i][1] = baseLidaA.iloc[i][1].replace(",", ".")
                    baseLidaA.iloc[i][1] = float(baseLidaA.iloc[i][1])

                check = re.search(r"(\W*\d*\W*\d*\W*\d*\W*\d*\W*\d*\W*\d*)(-$)", str(baseLidaA.iloc[i][2]))
                if check:
                    baseLidaA.iloc[i][2] = check.group(2) + check.group(1)

                if not(pd.isnull(baseLidaA.iloc[i][2]) or baseLidaA.iloc[i][2] == "CORRECAO/JUROS" or baseLidaA.iloc[i][2] == "(+)"
                    or baseLidaA.iloc[i][2] == "(-)" or baseLidaA.iloc[i][2] == "(=)"):
                    baseLidaA.iloc[i][2] = baseLidaA.iloc[i][2].replace(".", "")
                    baseLidaA.iloc[i][2] = baseLidaA.iloc[i][2].replace(",", ".")

                    baseLidaA.iloc[i][2] = float(baseLidaA.iloc[i][2])

                check = re.search(r"(\W*\d*\W*\d*\W*\d*\W*\d*\W*\d*\W*\d*)(-$)", str(baseLidaA.iloc[i][3]))
                if check:
                    baseLidaA.iloc[i][3] = check.group(2) + check.group(1)

                if not (pd.isnull(baseLidaA.iloc[i][3]) or baseLidaA.iloc[i][3] == "TOTAL" or baseLidaA.iloc[i][
                    3] == "(+)"
                        or baseLidaA.iloc[i][3] == "(-)" or baseLidaA.iloc[i][3] == "(=)"):
                    baseLidaA.iloc[i][3] = baseLidaA.iloc[i][3].replace(".", "")
                    baseLidaA.iloc[i][3] = baseLidaA.iloc[i][3].replace(",", ".")

                    baseLidaA.iloc[i][3] = float(baseLidaA.iloc[i][3])


            baseLidaA.to_excel(f"~\\Documents\\{nomeArquivo}", index=False, sheet_name=tipoArquivo, header=False)
            arqsSucesso.append(arq)
            logging.info(f"O arquivo {arq} foi lido com sucesso")

        else:

            largurasColunasTipoB = [1, 13, 4, 15, 10, 17, 17, 17, 17, 17, 10, 4, 4, 6, 298]
            baseLidaB = pd.read_fwf(caminhoTotal, header=None, widths=largurasColunasTipoB, encoding='unicode_escape')

            nProcesso = 0

            baseLidaA['PROCESSO'] = nProcesso
            baseLidaB['PROCESSO'] = nProcesso


            dataArquivo = baseLidaA.loc[3, 1][-10:].replace(".", "_")
            nomeArquivo = f"{tipoArquivo} {dataArquivo}.xlsx"

            for i in range(len(baseLidaA)):

                if (str(baseLidaA.loc[i, 0]) == "A"):
                    baseLidaA.loc[i, 'PROCESSO'] = baseLidaA.loc[i - 1, 'PROCESSO'] + 1
                    baseLidaB.loc[i, 'PROCESSO'] = baseLidaB.loc[i - 1, 'PROCESSO'] + 1

                if (str(baseLidaA.loc[i, 0]) == "B"):
                    baseLidaA.loc[i, 'PROCESSO'] = baseLidaA.loc[i - 1, 'PROCESSO']
                    baseLidaB.loc[i, 'PROCESSO'] = baseLidaB.loc[i - 1, 'PROCESSO']

            baseLidaA = baseLidaA.drop(range(6))

            baseLidaA.columns = ["CODIGOA","NUMERO_DO_PROCESSO","NOME_DO_TRIBUNAL","NOME_DA_COMARCA","ORGAO","DEPENDENCIA",
                                "NOME_RECLAMANTE", "CPF_CNPJ_RECLAMANTE", "NOME_RECLAMADO", "CPF_CNPJ_RECLAMADO",
                                "FILLER", "PROCESSO"]

            baseLidaB = baseLidaB.drop(range(6))

            baseLidaB.columns = ["CODIGOB", "CONTA_JUDICIAL", "PARCELA", "NUMERO_DA_GUIA", "DATA_DO_DEPOSITO",
                                "VALOR_SALDO_CAPITAL", "VALOR_CORRECAO_MONETARIA",
                                "VALOR_JUROS", "VALOR_SALDO_CORRIGIDO", "VALOR_IR", "DATA_PROCESSAMENTO", "CD_PRD_BNC",
                                "NR_SEQUENCIAL_LEGISLACAO_TRIBUTARIA",
                                "NUMERO_LEI_TRIBUTARIA", "FILLER", "PROCESSO"]

            if(baseLidaA.iloc[0]["CODIGOA"]=="B" and baseLidaB.iloc[0]["CODIGOB"]=="B"):
                logging.error(f"O arquivo {arquivo_leitura} não pode ser carregado, verificar a integridade do arquivo")
                print("Base Com Problemas")
                return None

            basesjuntas = pd.merge(baseLidaA, baseLidaB, on="PROCESSO", how="left")

            basesjuntas = basesjuntas[(basesjuntas['CODIGOA'] == "A") & (basesjuntas['CODIGOB'] == "B")]

            basesjuntas = basesjuntas.drop(["CODIGOA", "CODIGOB", "FILLER_x", "FILLER_y", "PROCESSO"], axis=1)

            basesjuntas["VALOR_SALDO_CAPITAL"] = basesjuntas["VALOR_SALDO_CAPITAL"].astype(float)/100
            basesjuntas["VALOR_CORRECAO_MONETARIA"] = basesjuntas["VALOR_CORRECAO_MONETARIA"].astype(float)/100
            basesjuntas["VALOR_JUROS"] = basesjuntas["VALOR_JUROS"].astype(float)/100
            basesjuntas["VALOR_SALDO_CORRIGIDO"] = basesjuntas["VALOR_SALDO_CORRIGIDO"].astype(float)/100

            if not basesjuntas.iloc[:]["VALOR_IR"].any():
                basesjuntas.iloc[:]["VALOR_IR"] = 0
            else:
                basesjuntas["VALOR_IR"] = basesjuntas.iloc[:]["VALOR_IR"].astype(float)/100


            if not basesjuntas.iloc[:]["DATA_PROCESSAMENTO"].any():
                basesjuntas.iloc[:]["DATA_PROCESSAMENTO"] = 0
            else:
                basesjuntas["DATA_PROCESSAMENTO"] = pd.to_datetime(basesjuntas["DATA_PROCESSAMENTO"], format='%d.%m.%Y')

            if not basesjuntas.iloc[:]["DATA_DO_DEPOSITO"].any():
                basesjuntas.iloc[:]["DATA_DO_DEPOSITO"] = 0
            else:
                basesjuntas["DATA_DO_DEPOSITO"] = pd.to_datetime(basesjuntas["DATA_DO_DEPOSITO"], format='%d.%m.%Y')

            basesjuntas["DATA_MOVIMENTO"] = pd.to_datetime(dataArquivo, format='%d_%m_%Y')
            basesjuntas["ARQUIVO"] = caminhoTotal.split("\\")[len(caminhoTotal.split("\\"))-1]
            basesjuntas["TIPO_ARQUIVO"] = tipoArquivo

            try:
                destino = lblDestino.cget("text")
                basesjuntas.to_excel(f"{destino}/{nomeArquivo}.xlsx", index=False, sheet_name=tipoArquivo)
                arqsSucesso.append(arq)

            except:
                logging.error(f"O arquivo {arq} não pode pode ser escrito em .xlsx, verificar permissão ou espaço em disco.")
                arqsFalha.append(arq)

            logging.info(f"O arquivo {arq} foi lido com sucesso")
    if len(arqsFalha)==0:
        messagebox.showinfo("Processamento Concluído", "Os seguinte arquivos foram processados com sucesso: "+", ".join(arqsSucesso))
    else:
        messagebox.showinfo("Processamento Concluído", "Os seguintes arquivos foram processados com sucesso: "+", ".join(arqsSucesso)+"\\n"+
                            "Os arquivos não tiveram sucesso no seu processamento: "+", ".join(arqsFalha))
def encerrar():
    window.destroy()

window = ct.CTk()
window.title("SADJud")
w = 760
h = 520
ws = window.winfo_screenwidth()
hs = window.winfo_screenheight()
x = (ws/2)-(w/2)
y = (hs/2)-(h/2)
window.geometry('%dx%d+%d+%d' % (w, h, x, y))
stringVarOrigem = tk.StringVar(window)
stringVarOrigem.set("Origem")
lblOrigem = tk.Label(window, bg = "white", width=70, bd = 4, relief="sunken")
lblOrigem.place(x = 200, y = 101)
origemArqs = ct.CTkButton(window, text="Origem dos Arquivos", command=origem)
origemArqs.place(x = 40, y = 100)

lblDestino = tk.Label(window, bg = "white", width=70, bd = 4, relief="sunken")
lblDestino.place(x = 200, y = 301)
destArqs = ct.CTkButton(window, text="Destino dos Arquivos", command=destino)
destArqs.place(x = 40, y = 300)      

processar = ct.CTkButton(window, text="Processar Arquivos", command=leitura_arquivo)
processar.place(x = 300, y = 400)

sair = ct.CTkButton(window, text="Encerrar SADJud", command=encerrar)
sair.place(x = 300, y = 450)



window.mainloop()
