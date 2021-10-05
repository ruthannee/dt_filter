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
dataset = dataset.drop(dataset[dataset.Clean == False].index)
print("Após 1º filtro: ", len(dataset), " registros.", "\n", "-" * 50)
# #Removendo registros com valores diferentes de "Yes" da coluna ATB
print("Valores da coluna ATB: \n", dataset.ATB.unique(), "\n")
dataset = dataset.drop(dataset[dataset.ATB != "Yes"].index)
print("Após 2º filtro: ", len(dataset), " registros.", "\n", "-" * 50)

del dataset['Clean']

#EXPORTAÇÃO 1
dataset.to_excel('New Produccion.xlsx', sheet_name="PN", header=True, index=False)