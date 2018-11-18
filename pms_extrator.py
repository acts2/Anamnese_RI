from bs4 import BeautifulSoup as bs
import requests
import re
import msf_extrator

pms_list = ['http://portalms.saude.gov.br/saude-de-a-z/tuberculose', 
'http://portalms.saude.gov.br/saude-de-a-z/sifilis-2', 'http://portalms.saude.gov.br/saude-de-a-z/malaria', 
'http://portalms.saude.gov.br/saude-de-a-z/leptospirose', 'http://portalms.saude.gov.br/saude-de-a-z/raiva', 
'http://portalms.saude.gov.br/saude-de-a-z/hantavirose', 'http://portalms.saude.gov.br/saude-de-a-z/febre-maculosa', 
'http://portalms.saude.gov.br/saude-de-a-z/caxumba', 'http://portalms.saude.gov.br/saude-de-a-z/asma',
'http://portalms.saude.gov.br/saude-de-a-z/botulismo']


def pmsScraping(start):
	end = start.find_next('h2')

	content = ''
	clean = ''
	

	item = start.find_next()
	while item != end:
		content += str(item)
		item = item.find_next()

	content = bs(content, 'html.parser')

	if start.get_text() == 'Tratamento':		
		paragraph = content.find('p')
		clean = msf_extrator.cleaning(str(paragraph))
	else:
		paragraph = content.find_all('p')
		lista = content.find_all('ul')
		clean = msf_extrator.cleaning(str(paragraph+lista))
	

	return clean

def scrap():
	pms_site = {}
	index = 21

	for link in pms_list:
		atr_values = []
		
		soup = msf_extrator.get_html(link)		
		

		def_start = soup.find('h1', {'class':'documentFirstHeading'})
		definicao = pmsScraping(def_start)
		atr_values.append(definicao)
		#print(definicao)
		

		sint = soup.find('h2', text= re.compile('^Sintomas'))
		sintomas = pmsScraping(sint)
		atr_values.append(sintomas)
		

		trat = soup.find('h2', text= re.compile('^Tratamento'))
		tratamento = pmsScraping(trat)
		atr_values.append(tratamento)
		#print(len(atr_values))

		atrValue = msf_extrator.atributos(atr_values)

		pms_site[index] = atrValue
		index += 1

	return pms_site






