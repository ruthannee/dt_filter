import pandas as pd
import numpy as np

#Importando o dataset
#dataset = pd.read_excel('\caminho do arquivo\\nome_do_arquivo.xlsx', sheet_name = "nome_da_pagina")
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
dsATENDE.to_excel('Fornecedores_A', sheet_name="Fornecedores", header=True, index=False)
dsNAO_ATENDE.to_excel('Fornecedores_NA.xlsx', sheet_name="Fornecedores", header=True, index=False)