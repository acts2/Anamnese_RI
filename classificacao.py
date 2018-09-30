"""
1° Passo - extrair o html dos links coletados
2° Passo - Prepara o dataset: Agrupar os rótulos e os textos e separá-los em dados de treinamento e dados de teste
3° Passo - Transformar os textos brutos em vetores de features para posteriormente serem classificados
4° Passo - Fazer seleção de features
5° Passo - Treinar o classificador com os métodos Naive Bayes, Decision Tree(j48), SVM(SMO), Logistic Regression(logistic), MLP
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
from sklearn import model_selection
def splitDataSet(dataFrame):
	train_text, test_text, train_label, test_label = model_selection.train_test_split(dataFrame['text'],dataFrame['labels'])

	return train_text, test_text, train_label, test_label


#transforma os textos em vetores de features para serem classificados
#tf-idf
from sklearn.feature_extraction.text import TfidfVectorizer
def tfidf(df,train_text,valid_text):
	vectorizer = TfidfVectorizer()
	vectorizer.fit(df['text'])
	train_transform = vectorizer.transform(train_text)
	valid_transform = vectorizer.transform(valid_text)
	#print(vectorizer.get_feature_names(train_transform))

	return train_transform, valid_transform

#feature selection
#estrategia: remover features com menor variância
from sklearn.feature_selection import VarianceThreshold

def selecao_features(features_train,features_test):
	sel = VarianceThreshold(threshold=(.8 * (1 - .8)))
	features_train_sel = sel.fit_transform(features_train)
	features_test_sel = sel.fit_transform(features_test)

	return features_train_sel, features_test_sel

#treinamento
#fazer um modelo de treinamento geral para todos os algoritmos 

def modelo_treinamento(classificador, vetor_treino, rotulos_treino,vetor_teste):
	clf = classificador
	clf.fit(vetor_treinamento,rotulos_treino)
	pred = clf.predict(vetor_teste)

	return pred

from sklearn.metrics import accuracy_score
def acuracia(pred,rotulos_teste):
	return accuracy_score(pred,rotulos_teste)






