import re
import logging
import sqlite3
import pandas as pd

base = pd.DataFrame('~\\Documents\\CONVENIO DE REPASSE DE DE 01_04_2024.xlsx')

print(base.head())
dataTeste = base.iloc[1]['DATA_MOVIMENTO']


banco = sqlite3.connect('djo.sqlite3')
cursor = banco.cursor()
cursor.execute('SELEC COUNT(*) FROM convenioderepasse WHERE'
 'DATA_MOVIMENTO==(%s)',dataTeste)

print(cursor.fetchall())
cursor.close()