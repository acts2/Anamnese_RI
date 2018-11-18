from bs4 import BeautifulSoup as bs
import requests
import re
import msf_extrator

ms_list = ['https://minutosaudavel.com.br/asma/', 'https://minutosaudavel.com.br/espondilite-anquilosante/',
 'https://minutosaudavel.com.br/catapora/', 'https://minutosaudavel.com.br/zika/', 'https://minutosaudavel.com.br/cancer-de-prostata/',
 'https://minutosaudavel.com.br/gota/', 'https://minutosaudavel.com.br/diverticulite/', 'https://minutosaudavel.com.br/rinite/',
 'https://minutosaudavel.com.br/tricomoniase/', 'https://minutosaudavel.com.br/fobia-social/']


def msScraping(start):
	end = start.find_next('h2')

	content = ''
	
	item = start.find_next()
	while item != end:
		content += str(item)
		item = item.find_next()

	content = bs(content, 'html.parser')

	paragraph = content.find_all('p')
	lista = content.find_all('ul')
	clean = msf_extrator.cleaning(str(paragraph+lista))
	

	return clean

def scrap():
	ms_site = {}
	index = 31

	for link in ms_list:
		atr_values = []
		
		soup = msf_extrator.get_html(link)		
		

		def_start = soup.find('a', {'id':'o-que-e'})
		definicao = msScraping(def_start)
		atr_values.append(definicao)
		#print(definicao)
		

		sint = soup.find('a', {'id':'sintomas'})
		sintomas = msScraping(sint)
		atr_values.append(sintomas)
		

		trat = soup.find('a', {'id':'tratamento'})
		tratamento = msScraping(trat)
		atr_values.append(tratamento)
		#print(len(atr_values))

		atrValue = msf_extrator.atributos(atr_values)

		ms_site[index] = atrValue
		index += 1

	return ms_site
