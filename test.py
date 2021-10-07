#SCRIPT (NÃO EXECUTAR)
dsATENDE['Part number'].iloc[0] #começa com '/'
dsATENDE['Part number'].iloc[75] #começa por número
dsATENDE['Part number'].values[0]

dsATENDE['Part number'].iloc[0].count('/')
dsATENDE['Part number'].values[0].count('/')

#Divide a string à partir da esquerda, usando um separador passado por parâmetro
dsATENDE['Part number'].iloc[0].split('/')
dsATENDE['Part number'].values[0].split('/')

dsATENDE['Part number'].iloc[0].startswith('/') #True
dsATENDE['Part number'].iloc[75].startswith('/') #False
dsATENDE['Part number'].values[0].startswith('/')

dsATENDE['Part number'].iloc[0].strip('/') #'305031/S2'
dsATENDE['Part number'].values[0].strip('/') #'305031/S2'

word = dsATENDE['Part number'].values[0] #'/305031/S2/'
word.count('/') #3
word.split("/")[0] #''
word.split("/")[1] #'305031'
word.split("/")[2] #'S2'
word.split("/")[3] #''
word.split("/")[1] + word.split("/")[2] #'305031S2'

word2 = dsATENDE['Part number'].values[75] #'1C35/2510130/AA/'
word2.split("/")[0] #'1C35'
word2.split("/")[1] #'2510130'
word2.split("/")[2] #'AA'
word2.split("/")[3] #''
word2.split("/")[0] + word2.split("/")[1] + word2.split("/")[2] + word2.split("/")[3] #'1C352510130AA'

word3 = dsATENDE['Part number'].values[259] #'2S65/A243W06/AB/35B'

pattern = '(?<=/).+?/'
result = re.search(pattern, word)
word[result.start():result.end() - 1] #'305031'

#remove todos os whitespaces da string
word.replace(" ", "")
#ou
re.sub(r"\s", "", word)