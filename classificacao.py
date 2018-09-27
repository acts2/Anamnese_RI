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

#divide o conjunto de dados entre conjunto de treinamento e validacao
def splitDataSet(dataFrame):
	train_text, test_text, train_label, test_label = model_selection.train_test_split(dataFrame['text'],dataFrame['labels'])

	return train_text, test_text


#transforma os textos em vetores de features para serem classificados
#tf-idf
from sklearn.feature_extraction.text import TfidfVectorizer
def tfidf(df,train_text,valid_text):
	vectorizer = TfidfVectorizer()
	vectorizer.fit(df['text'])
	train_transform = vectorizer.transform(train_text)
	valid_transform = vectorizer.transform(valid_text)
	print(vectorizer.get_feature_names(train_transform))

	return train_transform, valid_transform


