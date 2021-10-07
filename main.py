import pandas as pd
import numpy as np
import re

#Importando o dataset
dataset = pd.read_excel('Produccion.xlsx', sheet_name="PN")
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

word = dsATENDE['Part number'].values[0] #'/305031/S2/'
word2 = dsATENDE['Part number'].values[75] #'1C35/2510130/AA/'
word3 = dsATENDE['Part number'].values[259] #'2S65/A243W06/AB/35B'
word4 = "GU5A/96613A39/LC/"

def ident_func(word):
    word = word.strip('/')
    return re.sub('/', '', word) if word.count('/') == 1 else re.sub('/', '', word.rsplit('/', 1)[0])

print(ident_func(word)) #305031S2
print(ident_func(word2)) #1C352510130
print(ident_func(word3)) #2S65A243W06AB
print(ident_func(word4)) #GU5A96613A39