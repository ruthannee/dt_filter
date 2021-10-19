import pandas as pd
import numpy as np
import re
from xlsxwriter.utility import xl_rowcol_to_cell

#Importando o dataset
dataset = pd.read_excel('Produccion.xlsx', sheet_name="Part Numbers")
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
fornecedor = pd.read_excel('Fornecedores/Fornecedor.xlsm', sheet_name="FERRAMENTAS")
fornecedor.rename(columns={'Unnamed: 1' : 'Part number', 'Unnamed: 14' : 'Final status'}, inplace=True)
fornecedor = pd.DataFrame(fornecedor[['Part number', 'Final status']])
fornecedor = fornecedor.drop(fornecedor.index[[0]])
fornecedor['Part number'] = fornecedor['Part number'].str.upper()
fornecedor['Final status'] = fornecedor['Final status'].str.upper()
print("PRIMEIROS REGISTROS DO FORNECEDOR: \n", fornecedor.head())

dsATENDE['CONSTA'] = dsATENDE.apply(lambda df1: len(list(filter(lambda df2: df1['Part number'] in df2, fornecedor['Part number']))) > 0, axis=1)
dsNAO_ATENDE['CONSTA'] = dsNAO_ATENDE.apply(lambda df1: len(list(filter(lambda df2: df1['Part number'] in df2, fornecedor['Part number']))) > 0, axis=1)

dsATENDE = dsATENDE.drop(dsATENDE[dsATENDE['CONSTA'] == False].index)
dsNAO_ATENDE = dsNAO_ATENDE.drop(dsNAO_ATENDE[dsNAO_ATENDE['CONSTA'] == True].index)

for pn in dsATENDE.index:
    dsATENDE.loc[pn, 'PN Fornecedor'] = ', '.join(list(fornecedor[fornecedor['Part number'].str.contains(dsATENDE['Part number'][pn])]['Part number']))
    dsATENDE.loc[pn, 'Final status'] = ', '.join(list(fornecedor[fornecedor['Part number'].str.contains(dsATENDE['Part number'][pn])]['Final status']))

#EXPORTAÇÃO FINAL
writer = pd.ExcelWriter('Novo Fornecedores AT.xlsx', engine='xlsxwriter')
dsATENDE.to_excel(writer, sheet_name="Fornecedores", header=True, index=False)
dsNAO_ATENDE.to_excel('Novo Fornecedores NA.xlsx', sheet_name="Fornecedores", header=True, index=False)

workbook = writer.book
worksheet = writer.sheets['Fornecedores']
worksheet.set_zoom(100)
worksheet.set_column('A:D', 15)
worksheet.set_column('H:L', 15)
worksheet.set_column('M:N', 20)
number_rows = len(dsATENDE.index)
color_range = "N2:N{}".format(number_rows+1)
worksheet.set_column('E:G', None, None, {'hidden': True})
worksheet.set_column('J:K', None, None, {'hidden': True})

obsolete = workbook.add_format({'bg_color': '#FFC7CE',
                               'font_color': '#9C0006'})
active = workbook.add_format({'bg_color': '#C6EFCE',
                               'font_color': '#006100'})
worksheet.conditional_format(color_range, {'type':     'cell',
                                    'criteria': 'equal to',
                                    'value':    '"OBSOLETE"',
                                    'format':   obsolete})
worksheet.conditional_format(color_range, {'type':     'cell',
                                    'criteria': 'equal to',
                                    'value':    '"ACTIVE"',
                                    'format':   active})

writer.save()