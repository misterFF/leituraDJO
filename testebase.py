import sqlite3
import pandas as pd
from datetime import datetime

def deletarPlanilhaData(banco, tbl, dataTeste):
    try:
        banco = sqlite3.connect(banco)
        cursor = banco.cursor()
        cursor.execute(f"""DELETE FROM '{tbl}' WHERE
            DATA_MOVIMENTO = '{dataTeste}'""")
        banco.commit()
        cursor.close()
        banco.close()
    except:
        print("Não foi possível deletar os itens do banco")

def verificaData(banco, tbl, dataTeste):
    banco = sqlite3.connect(banco)
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
        banco = sqlite3.connect(banco)
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

def dataMaxima(banco, tbl):
    banco = sqlite3.connect(banco)
    cursor = banco.cursor()
    cursor.execute(f"""SELECT MAX(DATA_MOVIMENTO) FROM '{tbl}'""")
    data = cursor.fetchall()[0][0]
    return data

def retPorData(banco, tbl, data):
    banco = sqlite3.connect(banco)
    cursor = banco.cursor()
    cursor.execute(f"""SELECT * FROM '{tbl}'
                    WHERE DATA_MOVIMENTO = '{data}'""")
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
    return df

if __name__ == '__main__':
    banco = 'djo.sqlite3'
    data = "08/05/2024 00:00"
    date_format = datetime.strptime(data, '%d/%m/%Y %H:%M')
    #print(date_format)
    df = retPorData(banco, 'resgatescontraogoverno', date_format)

    #print(dataMaxima(banco, 'resgatescontraogoverno'))

    #tbl = 'resgatesafavordogoverno'
    #conn =sqlite3.connect(banco)
    #cursor = conn.cursor()
    #sqlStatement = f"""SELECT (DATA_MOVIMENTO) FROM '{tbl}'"""
    #sqlStatement = f"""ALTER TABLE '{tbl}' RENAME TO resgatesafavordogoverno"""
    #sqlStatement = f"""SELECT NUMERO_DO_PROCESSO, NOME_RECLAMANTE, CPF_CNPJ_RECLAMANTE, NOME_RECLAMADO, CPF_CNPJ_RECLAMADO, SUM(VALOR_SALDO_CORRIGIDO) FROM '{tbl}'
    #                    WHERE DATA_MOVIMENTO = '2024-05-08 00:00:00'
    #                    GROUP BY NUMERO_DO_PROCESSO
    #                    """
    #sqlStatement = f"""SELECT * FROM '{tbl}'"""

    #cursor.execute(sqlStatement)

    #for lin in cursor.fetchall():
    #    print(lin)





