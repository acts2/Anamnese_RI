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



from collections import defaultdict, Counter
import pandas
def create_index():

	tokens = preprocessing()
	index = defaultdict(list)
	ind = defaultdict(list)

	for i, token in tokens:
		for term in token:
			index[term].append(i)


	for k in index.keys():
		count = Counter(index[k])
		count = list(count.items())
		df = pandas.DataFrame(count, columns = ['DocID', 'Frequencia'])
		index[k] = count
		ind[k] = df

	return index, ind

def create_compression_index():
	tokens = preprocessing()
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
			aux.append(count[j] - count[j-1])
			j += 1


		index[k] = aux

	for k in index.keys():
		aux = list(zip(ind[k],index[k]))
		a = list(aux[0])
		a[1] = '-'
		aux[0] = tuple(a)
		df = pandas.DataFrame(aux, columns = ['DocID', 'Intervalo'])
		new_index[k] = df


	return index, new_index


def create_new_index():

	tokens = preprocessing_version2()
	index = defaultdict(list)

	for i, token in tokens:
		for term in token:
			index[term].append(i)

	for k in index.keys():
		count = Counter(index[k])
		count = list(count.items())		
		index[k] = count

	return index













