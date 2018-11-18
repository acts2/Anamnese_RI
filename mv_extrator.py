from bs4 import BeautifulSoup as bs
import requests
import re
import msf_extrator

# www.minhavida.com.br

mv_list = ['https://www.minhavida.com.br/saude/temas/anorexia', 'https://www.minhavida.com.br/saude/temas/cancer', 
'https://www.minhavida.com.br/saude/temas/anemia', 'https://www.minhavida.com.br/saude/temas/angioedema',
'https://www.minhavida.com.br/saude/temas/hepatite-b', 'https://www.minhavida.com.br/saude/temas/febre',
'https://www.minhavida.com.br/saude/temas/tumor-cerebral', 'https://www.minhavida.com.br/saude/temas/bulimia',
'https://www.minhavida.com.br/saude/temas/apneia-do-sono', 'https://www.minhavida.com.br/saude/temas/dengue']



def minhavida_scraping(start):

	end = start.find_next('h2')
	content = ''
	item = start.nextSibling
	while item != end:
  		content += str(item)
  		item = item.nextSibling

	content = bs(content, 'html.parser')
	paragraph = content.find_all('p', {'class':'paragraph'})
	lista = content.find_all('ul', {'class': 'paragraph bullet'})

	clean = msf_extrator.cleaning(str(paragraph+lista))

	return clean


def scrap():

	mv_site = {}
	index = 11
	for link in mv_list:
		atr_values = []
		soup = msf_extrator.get_html(link)
		title = soup.title.get_text().split(':')[0]
		oque = '\n    O que é {}?\n'.format(title)
		sin = '\n    Sintomas de {}\n'.format(title)
		dia = '\n    Diagnóstico de {}\n'.format(title)
		tr = '\n    Tratamento de {}\n'.format(title)

		def_start = soup.find('h2', text = oque)
		definicao = minhavida_scraping(def_start)
		#print(definicao)
		atr_values.append(definicao)		

		sint = soup.find('h2', text= sin)
		sintomas = minhavida_scraping(sint)
		atr_values.append(sintomas)

		
		trat = soup.find('h2', text= tr)
		tratamento = minhavida_scraping(trat)
		atr_values.append(tratamento)

		atrValue = msf_extrator.atributos(atr_values)

		mv_site[index] = atrValue
		index += 1

	return mv_site


