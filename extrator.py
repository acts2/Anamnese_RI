from bs4 import BeautifulSoup as bs
import requests
import re
import msf_extrator

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

all_links = mv_list + pms_list + ms_list + scuf_list

def msfScrap():

	msfSite = {}
	index = 1

	for link in msf_list:		
		content = msf_extrator.get_html(link)
		paragraph = str(content.find('div', {'class':'bl-esq'}))

		bl_dir = content.find_all('div', {'class':'bl-dir'})
		bl = list(bl_dir)
		
		for i in bl:		
			paragraph += str(i.find('p'))

		span = content.find_all('span')
		span = list(span)                                      
		for i in span:
			paragraph += str(i)

		paragraph += str(content.find('div', {'class':'atv-txt'}).find('p'))
		paragraph += str(content.find('section', {'class':'bl-atv-mdc'}).find('p'))

		clean = msf_extrator.cleaning(str(paragraph))

		msfSite[index] = clean
		index +=1

	return msfSite

def scrap():

	
	all_sites = {}
	msf = msfScrap()
	als = {}
	index = 11

	for link in all_links:

		content = msf_extrator.get_html(link)

		paragraph = content.find_all('p')
		lista = content.find_all('ul')
		clean = msf_extrator.cleaning(str(paragraph+lista))

		all_sites[index] = clean
		index +=1

	als = {**msf, **all_sites}

	return als








