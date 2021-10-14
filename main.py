import pandas as pd
import numpy as np
import re

#Importando o dataset
dataset = pd.read_excel('20210922 GSBDs_Produtivo_Fechamento (Produccion).xlsx', sheet_name="Part Numbers")
print(dataset.head(),"\n", "-" * 50)
print("Dataset inteiro: ", len(dataset), " registros.", "\n", "-" * 50)

#Uma coluna "Clean" é criada, atribuindo TRUE para a condição
dataset['Clean'] = np.logical_and(dataset['ATB'] == "Yes", dataset['Program Pending'] == 0)
print("Quantidade total de registros por valor TRUE e FALSE: \n", dataset['Clean'].value_counts().to_string(), "\n", "-" * 50)
#Registros que possuem valor TRUE são removidos, mantendo somente os registros que não obedecem a condição
dsATENDE = dataset.drop(dataset[dataset.Clean == False].index)
dsNAO_ATENDE = dataset.drop(dataset[dataset.Clean == True].index)

del dataset['Clean'] 
del dsATENDE['Clean'] 
del dsNAO_ATENDE['Clean']

#EXPORTAÇÃO 1
dsATENDE.to_excel('Fornecedores_A.xlsx', sheet_name="Fornecedores", header=True, index=False)
dsNAO_ATENDE.to_excel('Fornecedores_NA.xlsx', sheet_name="Fornecedores", header=True, index=False)

def ident_func(word):
    word = word.strip('/')
    return re.sub('/', '', word) if word.count('/') == 1 else re.sub('/', '', word.rsplit('/', 1)[0])

dsATENDE['Part number'] = dsATENDE.apply(lambda r:  ident_func(r['Part number']), axis=1)
dsNAO_ATENDE['Part number'] = dsNAO_ATENDE.apply(lambda r:  ident_func(r['Part number']), axis=1)

#Planilha do fornecedor
fornecedor = pd.read_excel('Fornecedores/Teste.xlsx')
fornecedor['Part number'] = fornecedor['Part number'].str.upper()
fornecedor.head()

dsATENDE['CONSTA'] = dsATENDE.apply(lambda df1: len(list(filter(lambda df2: df1['Part number'] in df2, fornecedor['Part number']))) > 0, axis=1)
dsNAO_ATENDE['CONSTA'] = dsNAO_ATENDE.apply(lambda df1: len(list(filter(lambda df2: df1['Part number'] in df2, fornecedor['Part number']))) > 0, axis=1)

dsATENDE = dsATENDE.drop(dsATENDE[dsATENDE['CONSTA'] == False].index)
dsNAO_ATENDE = dsNAO_ATENDE.drop(dsNAO_ATENDE[dsNAO_ATENDE['CONSTA'] == True].index)

#retorna registros de CONSTA == True
fornecedor['FINAL'] = dsATENDE[~dsATENDE['Part number'].isin(fornecedor['Part number'])]['Part number'].values
print(fornecedor.columns)

dsATENDE = pd.merge(dsATENDE, fornecedor, how='inner', left_on='Part number', right_on='FINAL')
dsATENDE.rename(columns={'Part number_x' : 'Part number', 'Part number_y': 'PD Original'}, inplace=True)
del dsATENDE['FINAL']

#EXPORTAÇÃO FINAL
dsATENDE.to_excel('Novo Fornecedores AT.xlsx', sheet_name="Fornecedores", header=True, index=False)
dsNAO_ATENDE.to_excel('Novo Fornecedores NA.xlsx', sheet_name="Fornecedores", header=True, index=False)