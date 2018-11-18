from bs4 import BeautifulSoup as bs
import requests
import re
import msf_extrator


scuf_list = ['https://www.saudecuf.pt/mais-saude/doencas-a-z/faringite', 'https://www.saudecuf.pt/mais-saude/doencas-a-z/diabetes',
'https://www.saudecuf.pt/mais-saude/doencas-a-z/psoriase', 'https://www.saudecuf.pt/mais-saude/doencas-a-z/acne',
 'https://www.saudecuf.pt/mais-saude/doencas-a-z/anorexia', 'https://www.saudecuf.pt/mais-saude/doencas-a-z/glaucoma', 
 'https://www.saudecuf.pt/mais-saude/doencas-a-z/lupus', 'https://www.saudecuf.pt/mais-saude/doencas-a-z/bronquite',
 'https://www.saudecuf.pt/mais-saude/doencas-a-z/endometriose', 'https://www.saudecuf.pt/mais-saude/doencas-a-z/sarampo']


def scufScraping(start):
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
	scuf_site = {}
	index = 41

	for link in scuf_list:
		atr_values = []

		soup = msf_extrator.get_html(link)	

		def_start = soup.find('span', text = re.compile('^O que é '))
		definicao = scufScraping(def_start)
		atr_values.append(definicao)
		#print(definicao)		

		sint = soup.find('span', text = re.compile('^Como se manifesta ') )
		sintomas = scufScraping(sint)
		atr_values.append(sintomas)		

		trat = soup.find('span', text = re.compile('^Como se trata '))
		tratamento = scufScraping(trat)
		atr_values.append(tratamento)
		#print(len(atr_values))

		atrValue = msf_extrator.atributos(atr_values)

		scuf_site[index] = atrValue
		index += 1

	return scuf_site




