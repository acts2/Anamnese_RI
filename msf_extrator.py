from bs4 import BeautifulSoup as bs
import requests
import re

msf_list = ['https://www.msf.org.br/o-que-fazemos/atividades-medicas/febre-amarela', 
'https://www.msf.org.br/o-que-fazemos/atividades-medicas/colera', 'https://www.msf.org.br/o-que-fazemos/atividades-medicas/hepatite-c',
'https://www.msf.org.br/o-que-fazemos/atividades-medicas/hivaids', 'https://www.msf.org.br/o-que-fazemos/atividades-medicas/sarampo',
'https://www.msf.org.br/o-que-fazemos/atividades-medicas/tuberculose', 'https://www.msf.org.br/o-que-fazemos/atividades-medicas/malaria',
'https://www.msf.org.br/o-que-fazemos/atividades-medicas/meningite', 
'https://www.msf.org.br/o-que-fazemos/atividades-medicas/doenca-de-chagas']

def get_html(link):
	response = requests.get(link)
	soup = bs(response.text, 'html.parser')

	return soup

def cleaning(raw_html):
	clean = re.compile('<.*?>')
	cleantext = re.sub(clean,'', raw_html)
	cleantext = re.sub(r'\n', ' ', cleantext)
	return cleantext

def msfScraping(start, title):
	end = start.find_next('section')
	#print(end)
	content = ''
	if start.get_text() == title:
		content = str(start.find_parent().find('p'))
		content += str(start.find_next('div',{'class':'bl-dir'}).find('p'))
	elif start.get_text() == 'Tratamento':
		content = str(start.find_parent().find('p'))
		content += str(start.find_parent().find('span'))		
	else:
		content = str(start.find_next('div',{'class':'bl-dir'}).find('p'))

	
	clean = cleaning(content)

	return clean

import pandas

def atributos(lista):	
	dic = {'definicao':lista[0], 'sintomas':lista[1], 'tratamento':lista[2]}
	#df = pandas.DataFrame(dic)
	return dic

def scrap(lista):

	msf_site = {}
	index = 1
	for link in lista:
		atr_values = []
		
		soup = get_html(link)		
		title = soup.find('div', {'class':'bl-esq'}).find_next().get_text()

		def_start = soup.find('h2', text = title)
		definicao = msfScraping(def_start,title)
		atr_values.append(definicao)
		#print(definicao)

		

		sint = soup.find('h2', text= 'Sintomas')
		sintomas = msfScraping(sint,title)
		atr_values.append(sintomas)

		
		trat = soup.find('h2', text= 'Tratamento')
		tratamento = msfScraping(trat,title)
		atr_values.append(tratamento)
		#print(len(atr_values))

		atrValue = atributos(atr_values)

		msf_site[index] = atrValue
		index += 1

	return msf_site


msf = scrap(msf_list)


