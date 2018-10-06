"""
1° Passo - extrair o html dos links coletados ok 
2° Passo - Prepara o dataset: Agrupar os rótulos e os textos e separá-los em dados de treinamento e dados de teste ok
3° Passo - Transformar os textos brutos em vetores de features para posteriormente serem classificados ok
4° Passo - Fazer seleção de features ok
5° Passo - Treinar o classificador com os métodos Naive Bayes, Decision Tree(j48), SVM(SMO), Logistic Regression(logistic), MLP ok
"""
import pickle
import numpy
# extrair o html dos links 
import requests 
from bs4 import BeautifulSoup as bs

def getHTML(link_list):
	htlmList = []
	n = 1
	for link in link_list:
		response = requests.get(link)
		print(type(response.text), n)
		n = n+1
		
		#soup = bs(response.text,'html.parser')
		htlmList.append(response.text)

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
from sklearn import model_selection
def splitDataSet(dataFrame):
	train_text, test_text, train_label, test_label = model_selection.train_test_split(dataFrame['text'],dataFrame['labels'])

	return train_text, test_text, train_label, test_label


#transforma os textos em vetores de features para serem classificados
#tf-idf
from sklearn.feature_extraction.text import TfidfVectorizer
def tfidf(df,train_text,valid_text):
	vectorizer = TfidfVectorizer()
	#vectorizer.fit(df['text'])
	train_transform = vectorizer.fit_transform(train_text)
	valid_transform = vectorizer.transform(valid_text)
	#print(vectorizer.get_feature_names(train_transform))

	return train_transform, valid_transform

#feature selection
#estrategia: remover features com menor variância
from sklearn.feature_selection import SelectPercentile, f_classif

def selecao_features(features_train,features_test,labels_train):
	sel = SelectPercentile(f_classif, percentile = 10)
	sel.fit(features_train, labels_train)
	features_train_sel = sel.transform(features_train).toarray()
	features_test_sel = sel.transform(features_test).toarray()

	print(len(features_train_sel),len(features_test_sel))

	return features_train_sel, features_test_sel

#treinamento
#fazer um modelo de treinamento geral para todos os algoritmos 

def modelo_treinamento(classificador, vetor_treino, rotulos_treino,vetor_teste):
	clf = classificador
	clf.fit(vetor_treino,rotulos_treino)
	pred = clf.predict(vetor_teste)

	return pred

from sklearn.metrics import accuracy_score
def acuracia(pred,rotulos_teste):
	acuracia = accuracy_score(pred,rotulos_teste)
	return acuracia


#pre-processamento

def abre():
	#carrega o arquivo
	data = open('C:/Users/Carolina Tavares/Documents/Anamnese_RI/rotulos.txt').read()
	rotulos = []
	links = []

	for i, line in enumerate(data.split("\n")):
		content = line.split()
		#print(type(content[1]))	
		rotulos.append(content[0])
		links.append(str(content[1]))

	rotulos[0] = rotulos[0][3:]

	return rotulos, links

from sklearn.naive_bayes import GaussianNB
def preprocessing():

	html = []

	#abre o arquivo com os rótulos e os respectivos links
	label, link = abre()
	print(len(label),len(link))

	#pega o html dos links
	html = getHTML(link)
	#print(type(html[0]))
	#html1 = getHTML(link[21:40:])


	df = getDataFrame(html,label)

	train_T, valid_T, train_L, test_L = splitDataSet(df)

	train_text_transform, valid_text_transform = tfidf(df,train_T,valid_T)

	train_sel, valid_sel = selecao_features(train_text_transform, valid_text_transform,train_L)

	predict = modelo_treinamento(GaussianNB(),train_sel, train_L,valid_sel)

	acc = acuracia(predict, test_L)

	

	return predict, acc, test_L
	

























