""" o que é 
    causas X
    diagnóstico X
    tratamento 
    sintomas"""

import mv_extrator, msf_extrator, pms_extrator, ms_extrator, scuf_extrator, extrator, pandas
import re 


msf = msf_extrator.scrap()
mv = mv_extrator.scrap()
pms = pms_extrator.scrap()
ms = ms_extrator.scrap()
scuf = scuf_extrator.scrap()

all_docs = {**msf, **mv, **pms, **ms, **scuf}

ext = extrator.scrap()




def tokeniza(st):
	out = re.sub(r'[^\w\s]',' ',st)
	out = out.split()
	out = list(map(str.lower,out))
	return out


def concatena(lista,key):
	out = []
	for st in lista:
		new_st = st+"."+key
		#par = (new_st, doc)
		out.append(new_st)

	return out

def remove(duplicate): 
    final_list = [] 
    for num in duplicate: 
        if num not in final_list: 
            final_list.append(num) 
    return final_list 

def preprocessing():	
	
	doc = []	

	for i in all_docs.keys():
		doci = []		
		for j in all_docs[i].keys():
			aux = concatena(tokeniza(all_docs[i][j]),j)
			doci += aux
		par = (i,doci)
		doc.append(par)

	return doc

def preprocessing_version2():

	doc = []

	for i in ext.keys():
		doci = []
		doci = tokeniza(ext[i])
		par = (i,doci)
		doc.append(par)

	return doc


"""
	Eu modifiquei os índices e agora o índice sem compressão retorna todos os ids mesmo se forem repetidos.
	Já o com compressão retorna só os intervalos, sem repetições
"""

from collections import defaultdict, Counter
import pandas
def create_index_aux(tokens):
	
	index = defaultdict(list)
	ind = defaultdict(list)

	for i, token in tokens:
		for term in token:
			index[term].append(i) #lista com os ids, com repetições


	for k in index.keys():
		count = Counter(index[k])
		count = list(count.items())
		df = pandas.DataFrame(count, columns = ['DocID', 'Frequencia'])
		#index[k] = count
		ind[k] = df #dataframe com ids e frequencia, sem repetições

	return index, ind

def create_compression_index_aux(tokens):
	
	index = defaultdict(list)
	ind = defaultdict(list)
	new_index = defaultdict(list)

	for i, token in tokens:
		for term in token:
			index[term].append(i)
			ind[term].append(i)

	
	for k in index.keys():
		j = 1 
		count = index[k]
		aux = []
		aux.append(count[0])		
		while j < len(count):
			if (count[j] - count[j-1]) != 0:
				aux.append(count[j] - count[j-1])
			
			j += 1
		index[k] = aux #lista com os intervalos, sem repetições

	
	for k in index.keys():
		temp = remove(ind[k])
		aux = list(zip(temp,index[k]))
		a = list(aux[0])
		a[1] = '-'
		aux[0] = tuple(a)
		df = pandas.DataFrame(aux, columns = ['DocID', 'Intervalo'])
		new_index[k] = df #dataframe contendo ids e intervalos, sem repetições


	return index, new_index


def create_index():
	tokens = preprocessing()
	return create_index_aux(tokens)

def create_index_2():
	tk = preprocessing_version2()
	return create_index_aux(tk)

def create_compression_index():
	tokens = preprocessing()
	return create_compression_index_aux(tokens)

def create_compression_index_2():
	tk = preprocessing_version2()
	return create_compression_index_aux(tk)



"""
	Eu fiz uma função pra medir o tamanho dos índices de acordo com o termo
	ex: medir_tamanho('vírus')
	Tamanho do índice sem compressão:  217

	Tamanho do índice com compressão:  28

	Diferença:  189
"""
def medir_tamanho(term):
	index, i, inter = {}, {}, {}

	if (bool(re.match(r'^\w+[\W]\w+$',term))): #verifica se o termo está concatenado
		index, i = create_index()
		inter, i = create_compression_index()
	else:
		index, i = create_index_2()
		inter, i = create_compression_index_2()
	

	print("Tamanho do índice sem compressão: ", len(index[term]))
	print("\nTamanho do índice com compressão: ", len(inter[term]))
	print("\nDiferença: ", (len(index[term]) - len(inter[term])))


	
	



	
















