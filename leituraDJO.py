import re
import logging
import sqlite3

def leitura_arquivo(arquivo_leitura):
    import pandas as pd
    logging.basicConfig(level=logging.INFO, filename="programa_2.log", format="%(asctime)s - %(levelname)s - %(message)s")
    largurasColunasTipoA = [1, 25, 25, 25, 25, 4, 30, 14, 30, 14, 257]
    caminhoTotal = arquivo_leitura

    baseLidaA = pd.read_fwf(caminhoTotal, header=None, widths=largurasColunasTipoA, encoding='unicode_escape')

    tipoArquivo = baseLidaA.loc[5, 1]

    if tipoArquivo == "RESUMO DO MOVIMENTO DIARI":

        largurasColunasTipoA = [37, 22, 27, 27]
        baseLidaA = pd.read_fwf(caminhoTotal, header=None, widths=largurasColunasTipoA, encoding='unicode_escape')
        dataArquivo = baseLidaA.loc[3, 0][-10:].replace(".", "_")
        nomeArquivo = f"{tipoArquivo} {dataArquivo}.xlsx"
#       nomeArquivo = tipoArquivo + " " + dataArquivo + ".xlsx"

        baseLidaA = baseLidaA.drop(range(6))
        baseLidaA.iloc[0][0] = "Data"
        baseLidaA.iloc[0][1] = dataArquivo
        #(\d{0,3}[.,]\d{0,3}[.,]\d{0,3}[.,]\d{0,3}[.,]\d{0,3})

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
        logging.info(f"O arquivo {arquivo_leitura} foi lido com sucesso")
        return baseLidaA

    else:

        largurasColunasTipoB = [1, 13, 4, 15, 10, 17, 17, 17, 17, 17, 10, 4, 4, 6, 298]
        baseLidaB = pd.read_fwf(caminhoTotal, header=None, widths=largurasColunasTipoB, encoding='unicode_escape')

        nProcesso = 0

        baseLidaA['PROCESSO'] = nProcesso
        baseLidaB['PROCESSO'] = nProcesso


        dataArquivo = baseLidaA.loc[3, 1][-10:].replace(".", "_")
        nomeArquivo = f"{tipoArquivo} {dataArquivo}.xlsx"
        #tipoArquivo + " " + dataArquivo + ".xlsx"

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
        #basesjuntas["DATA DO DEPOSITO"] = pd.to_datetime(basesjuntas["DATA DO DEPOSITO"], format='%d.%m.%Y')

        basesjuntas["DATA_MOVIMENTO"] = pd.to_datetime(dataArquivo, format='%d_%m_%Y')
        basesjuntas["ARQUIVO"] = caminhoTotal.split("\\")[len(caminhoTotal.split("\\"))-1]
        basesjuntas["TIPO_ARQUIVO"] = tipoArquivo

        try:
            basesjuntas.to_excel(f"~\\Documents\\{nomeArquivo}", index=False, sheet_name=tipoArquivo)

        except:
            logging.error(f"O arquivo {arquivo_leitura} não pode pode ser escrito em .xlsx, verificar permissão ou espaço em disco.")

        logging.info(f"O arquivo {arquivo_leitura} foi lido com sucesso")
        return basesjuntas

def conectaBanco(banco):
    try:
        conexao = sqlite3.connect(banco)
        return conexao
    except:
        print("Não foi possível acessar o banco")
        return None
def deletarPlanilhaData(banco, tbl, dataTeste):
    try:
        cursor = banco.cursor()
        cursor.execute(f"""DELETE FROM '{tbl}' WHERE
            DATA_MOVIMENTO = '{dataTeste}'""")
        banco.commit()
        cursor.close()
        banco.close()
    except:
        print("Não foi possível deletar os itens do banco")

def verificaData(banco, tbl, dataTeste):
    cursor = banco.cursor()
    cursor.execute(f"""SELECT COUNT(CONTA_JUDICIAL) FROM '{tbl}' WHERE
     DATA_MOVIMENTO = '{dataTeste}'""")
    cntDados = (int(cursor.fetchall()[0][0]))
    cursor.close()
    banco.close()
    if cntDados > 0:
        return True
    else:
        return False

def adicionarPlanilhaData(banco, tbl, base):
    try:
        cursor = banco.cursor()
        cursor.execute(f"""create table if not exists '{tbl}' (
                                   NUMERO_DO_PROCESSO text,
                                   NOME_DO_TRIBUNAL text,
                                   NOME_DA_COMARCA text,
                                   ORGAO text,
                                   DEPENDENCIA text,
                                   NOME_RECLAMANTE text,
                                   CPF_CNPJ_RECLAMANTE text,
                                   NOME_RECLAMADO text,
                                   CPF_CNPJ_RECLAMADO text,
                                   CONTA_JUDICIAL text,
                                   PARCELA text,
                                   NUMERO_DA_GUIA text,
                                   DATA_DO_DEPOSITO date,
                                   VALOR_SALDO_CAPITAL float,
                                   VALOR_CORRECAO_MONETARIA float,
                                   VALOR_JUROS float,
                                   VALOR_SALDO_CORRIGIDO float,
                                   VALOR_IR float,
                                   DATA_PROCESSAMENTO date,
                                   CD_PRD_BNC text,
                                   NR_SEQUENCIAL_LEGISLACAO_TRIBUTARIA text,
                                   NUMERO_LEI_TRIBUTARIA text,
                                   DATA_MOVIMENTO date,
                                   ARQUIVO text,
                                   TIPO_ARQUIVO)""")
        base.to_sql(tbl, banco, if_exists='append', index=False)
        banco.commit()
        cursor.close()
        banco.close()
    except:
        print("Não foi possível adicionar dados novos na planilha")

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    import os
    #caminho = "\\\\cifs-zone3\\transfarq\\SATE\\djo\\2024\\02 - Fevereiro\\Arquivos DJO\\"
    caminho = "C:\\Users\\fsilva3\\Documents\\Arquivoslidos\\"
    #caminho = "C:\\Users\\Flavio Silva\\Documents\\ArquivosConvenio\\"
    banco = 'djo.sqlite3'
    substiuirDados = "NÃO"
    arquivos = os.listdir(caminho)

    for arq in arquivos:
        caminhoTotal = caminho + arq
        base = leitura_arquivo(caminhoTotal)
        print(arq)
        data = str(base.loc[1, 'DATA_MOVIMENTO'])
        print(data)
        if base.iloc[0]["TIPO_ARQUIVO"].count("DEPOSITOS"):
            tbl = 'depositosacolhidos'
            conexao = conectaBanco(banco)
            if verificaData(conexao, tbl, data) == False:
                adicionarPlanilhaData(conexao, tbl, base)
            else:
                if substiuirDados == "SIM":
                    deletarPlanilhaData(conexao, tbl, data)
                    adicionarPlanilhaData(conexao, tbl, base)
                else:
                    None

        elif base.iloc[0]["TIPO_ARQUIVO"].count("FAVOR"):
            tbl = 'regatesafavordogoverno'
            conexao = conectaBanco(banco)
            if verificaData(conexao, tbl, data) == False:
                adicionarPlanilhaData(conexao, tbl, base)
            else:
                if substiuirDados == "SIM":
                    deletarPlanilhaData(conexao, tbl, data)
                    adicionarPlanilhaData(conexao, tbl, base)
                else:
                    None

        elif base.iloc[0]["TIPO_ARQUIVO"].count("CONTRA"):
            tbl = 'regatescontraogoverno'
            conexao = conectaBanco(banco)
            if verificaData(conexao, tbl, data) == False:
                adicionarPlanilhaData(conexao, tbl, base)
            else:
                if substiuirDados == "SIM":
                    deletarPlanilhaData(conexao, tbl, data)
                    adicionarPlanilhaData(conexao, tbl, base)
                else:
                    None

        elif base.iloc[0]["TIPO_ARQUIVO"].count("CONVENIO"):
            tbl = 'convenioderepasses'
            conexao = conectaBanco(banco)
            if verificaData(conexao, tbl, data) == False:
                adicionarPlanilhaData(conexao, tbl, base)
            else:
                if substiuirDados == "SIM":
                    deletarPlanilhaData(conexao, tbl, data)
                    adicionarPlanilhaData(conexao, tbl, base)
                else:
                    None
        else:
            print("Arquivo de resumo de movimentação")  