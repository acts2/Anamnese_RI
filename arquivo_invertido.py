""" o que é 
    causas 
    diagnóstico
    tratamento 
    sintomas"""

msf_list = ['https://www.msf.org.br/o-que-fazemos/atividades-medicas/febre-amarela', 
'https://www.msf.org.br/o-que-fazemos/atividades-medicas/colera', 'https://www.msf.org.br/o-que-fazemos/atividades-medicas/hepatite-c',
'https://www.msf.org.br/o-que-fazemos/atividades-medicas/hivaids', 'https://www.msf.org.br/o-que-fazemos/atividades-medicas/sarampo',
'https://www.msf.org.br/o-que-fazemos/atividades-medicas/tuberculose', 'https://www.msf.org.br/o-que-fazemos/atividades-medicas/malaria',
'https://www.msf.org.br/o-que-fazemos/atividades-medicas/meningite', 
'https://www.msf.org.br/o-que-fazemos/atividades-medicas/doenca-de-chagas', 'https://www.msf.org.br/o-que-fazemos/atividades-medicas/chikungunya']

mv_list = ['https://www.minhavida.com.br/saude/temas/anorexia', 'https://www.minhavida.com.br/saude/temas/cancer', 
'https://www.minhavida.com.br/saude/temas/anemia', 'https://www.minhavida.com.br/saude/temas/angioedema',
'https://www.minhavida.com.br/saude/temas/hepatite-b', 'https://www.minhavida.com.br/saude/temas/febre',
'https://www.minhavida.com.br/saude/temas/tumor-cerebral', 'https://www.minhavida.com.br/saude/temas/bulimia',
'https://www.minhavida.com.br/saude/temas/apneia-do-sono', 'https://www.minhavida.com.br/saude/temas/dengue']

pms_list = ['http://portalms.saude.gov.br/saude-de-a-z/tuberculose', 
'http://portalms.saude.gov.br/saude-de-a-z/sifilis-2', 'http://portalms.saude.gov.br/saude-de-a-z/malaria', 
'http://portalms.saude.gov.br/saude-de-a-z/leptospirose', 'http://portalms.saude.gov.br/saude-de-a-z/raiva', 
'http://portalms.saude.gov.br/saude-de-a-z/hantavirose', 'http://portalms.saude.gov.br/saude-de-a-z/febre-maculosa', 
'http://portalms.saude.gov.br/saude-de-a-z/caxumba', 'http://portalms.saude.gov.br/saude-de-a-z/asma',
'http://portalms.saude.gov.br/saude-de-a-z/botulismo']

ms_list = ['https://minutosaudavel.com.br/asma/', 'https://minutosaudavel.com.br/espondilite-anquilosante/',
 'https://minutosaudavel.com.br/catapora/', 'https://minutosaudavel.com.br/zika/', 'https://minutosaudavel.com.br/cancer-de-prostata/',
 'https://minutosaudavel.com.br/gota/', 'https://minutosaudavel.com.br/diverticulite/', 'https://minutosaudavel.com.br/rinite/',
 'https://minutosaudavel.com.br/tricomoniase/', 'https://minutosaudavel.com.br/fobia-social/']

scuf_list = ['https://www.saudecuf.pt/mais-saude/doencas-a-z/faringite', 'https://www.saudecuf.pt/mais-saude/doencas-a-z/diabetes',
'https://www.saudecuf.pt/mais-saude/doencas-a-z/psoriase', 'https://www.saudecuf.pt/mais-saude/doencas-a-z/acne',
 'https://www.saudecuf.pt/mais-saude/doencas-a-z/anorexia', 'https://www.saudecuf.pt/mais-saude/doencas-a-z/glaucoma', 
 'https://www.saudecuf.pt/mais-saude/doencas-a-z/lupus', 'https://www.saudecuf.pt/mais-saude/doencas-a-z/bronquite',
 'https://www.saudecuf.pt/mais-saude/doencas-a-z/endometriose', 'https://www.saudecuf.pt/mais-saude/doencas-a-z/sarampo']


import mv_extrator, msf_extrator, pms_extrator, ms_extrator, scuf_extrator, pandas
import re 


msf = msf_extrator.scrap(msf_list)
mv = mv_extrator.scrap(mv_list)
pms = pms_extrator.scrap(pms_list)
ms = ms_extrator.scrap(ms_list)
scuf = scuf_extrator.scrap(scuf_list)

all_docs = {**msf, **mv, **pms, **ms, **scuf}



def tokeniza(st):
	out = re.sub(r'[^\w\s]','',st)
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


	return index, ind









