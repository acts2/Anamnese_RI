"""
1° Passo - extrair o html dos links coletados
2° Passo - Prepara o dataset: Agrupar os rótulos e os textos e separá-los em dados de treinamento e dados de teste
3° Passo - Transformar os textos brutos em vetores de features para posteriormente serem classificados
"""

# extrair o html dos links 
import requests 
from bs4 import BeautifulSoup as bs

def getHTML(link_list):
	htlmList = []
	for link in link_list:
		response = requests.get(link)
		soup = bs(response.text,'html.parser')
		htlmList.append(soup)

	return htlmList

# preparar o dataset
# falta rotular os links

import pandas

def getDataFrame(text_list,label_list):
	df = pandas.DataFrame()
	df['text'] = text_list
	df['labels'] = label_list

	return df


