# -*- coding: utf-8 -*-
"""Assignment_3_kNN

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/10rwmlTY6YYwo4jlZ3oFP3FZoPrSQ92ww
"""

import math
import random

import numpy as np
import pandas as pd

import string
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
# from bs4 import BeautifulSoup as bs
# import lxml
from sklearn.model_selection import train_test_split
from scipy.spatial import distance
from sklearn.metrics import confusion_matrix
from sklearn.metrics.pairwise import cosine_similarity

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('words')


import enum
from sklearn.metrics import classification_report
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics import hamming_loss
from sklearn.metrics.pairwise import manhattan_distances, cosine_similarity, euclidean_distances

class Metric(enum.Enum):
    EUCLIDEAN_DISTANCE = "euclidean"
    HAMMING_DISTANCE = "hamming"
    MANHATTAN_DISTANCE = "manhattan"
    COSINE_SIMILARITY = "cosine"

class kNN_Texts:

    # DO NOT change anything in the constructor
    def __init__(self, vectorizer_class = None, 
                 K = None,
                 metric = Metric.EUCLIDEAN_DISTANCE):
        
        self.__vectorizer = vectorizer_class(analyzer=lambda text: text)
        # self.__vectorizer = vectorizer_class(analyzer=self.__preprocess_text)
        
        self.__K = K
        self.__metric = metric

        self.__train_vocabulary = None
        self.__train_feature_vectors = None
        self.__train_labels = None

    """@staticmethod"""
    def __preprocess_text(self, texts): #take from your provided Notebook
        preprocessed_text = []
        for text in texts:
          #Lowercase the text
          text = text.lower()
          
          #Number Removal
          text = re.sub(r'[-+]?\d+', '', text) 
          
          #Remove hyperlinks
          text = re.sub(r'https?:\/\/\S*', '', text)
          text = re.sub(r'www\.\S*', '', text)
          text = re.sub(r'\S*\.(com|info|net|org)', '', text)
          
          #Remove punctuations
          text = text.translate((str.maketrans('', '', string.punctuation)))

          #Tokenize
          text = word_tokenize(text)
      
          #Remove stopwords
          stop_words = set(stopwords.words('english'))
          text = [word for word in text if not word in stop_words]

          #Lemmatize tokens
          lemmatizer = WordNetLemmatizer()
          text = [lemmatizer.lemmatize(word) for word in text]
          #Stemming tokens
          stemmer = PorterStemmer()
          text = [stemmer.stem(word) for word in text]
          preprocessed_text.append(text)
        return preprocessed_text


    def __fit_vectorizer(self, texts):
        # fit the attribute vectorizer
        # self.__vectorizer.fit(texts)
        # print("__fit_vectorizer: True or not", texts)
        texts = np.asarray(texts)
        # print("aftercoversion__fit_vectorizer: True or not", texts)
        vectorizer = self.__vectorizer.fit(texts)
        # print("vectorizer", vectorizer)
        self.__train_vocabulary = vectorizer.vocabulary_
        # print("Vocabulary:  ", vectorizer.vocabulary_)
        # vector = vectorizer.transform(texts).toarray()
        # print("Vector:  ", vector)
        return vectorizer


    def __vectorize_texts(self, texts):
        texts_feature_vectors = self.__fit_vectorizer(texts)
        texts_feature_vectors = texts_feature_vectors.transform(texts).toarray()
        # print("Vector:  ")
        # print(texts_feature_vectors)
        return texts_feature_vectors


    def __train(self, texts, labels):   
        preprocessed_texts = self.__preprocess_text(texts)
        # print("Train: ", preprocessed_texts)
        self.__fit_vectorizer(preprocessed_texts)
        train_feature_vectors = self.__vectorize_texts(preprocessed_texts)
        train_labels = np.asarray(labels)
       
        return train_feature_vectors, train_labels

    def fit(self, texts, labels):
        self.__train_feature_vectors, self.__train_labels = self.__train(texts=texts, 
                                                                         labels=labels)
  
    
    def __compute_metric_to_train_points(self, feature_vector):
        metric_values = None

        if self.__metric == Metric.EUCLIDEAN_DISTANCE:
            metric_values = [] 
            for vec in self.__train_feature_vectors:
              # print("self.__train_feature_vectors[vec]: ", self.__train_feature_vectors[vec])
              # vec = vec.tolist()
              # feature_vector = feature_vector.tolist()
              # print("[vec, feature_vector]=>", [vec, feature_vector])
              x = euclidean_distances([vec], [feature_vector])
              # x = euclidean_distances([[1,2,3,4,5], [1,5,6,8,4]])
              metric_values.append(x)
        elif self.__metric == Metric.HAMMING_DISTANCE:
            metric_values = [] 
            for vec in self.__train_feature_vectors:
              x = hamming_loss([vec], [feature_vector])
              metric_values.append(x)

        elif self.__metric == Metric.MANHATTAN_DISTANCE:
            metric_values = [] 
            for vec in self.__train_feature_vectors:
              x = manhattan_distances([vec], [feature_vector])
              metric_values.append(x)

        elif self.__metric == Metric.COSINE_SIMILARITY:
            metric_values = [] 
            for vec in self.__train_feature_vectors:
              x = cosine_similarity([vec], [feature_vector])
              metric_values.append(x)

        return metric_values

    
    def predict(self, texts):
      predictions = []

      preprocessed_texts = self.__preprocess_text(texts)

      # print("preprocessed_texts: ", preprocessed_texts)

      test_feature_vectors = self.__vectorize_texts(preprocessed_texts)

      # print("test_feature_vectors: ", test_feature_vectors)
      for i in range(len(test_feature_vectors)):
        dist = []
        for tf in self.__train_feature_vectors:
          # print("test_feature_vectors[i]: ", test_feature_vectors[i])
          # test_feature_vectors = np.array(test_feature_vectors[i])
          d = (self.__compute_metric_to_train_points(test_feature_vectors[i]))
          dist.append(d)

        if self.__metric != 'cosine':
          dist.sort()
        else:
          dist.sort(reverse=True)
        dist = np.asarray(dist).flatten()

        knn = dist[:self.__K+1]

        p = 0
        for k in knn:
          if k != 0:
            # print("k: ", k)
            if self.__train_labels[i] == 0:
              p += (1/k) * -1 # What you discussed in the class (-1, 1)
            else:
              p += (1/k) * 1
          else:
            continue
        
        if p < 0:
          predictions.append(0)
        else:
          predictions.append(1)
      return predictions

train = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/Assignment_3/train.csv')
test = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/Assignment_3/test.csv')
train.reset_index(inplace=True)
test.reset_index(inplace=True)
train = train.drop(columns=['id'], axis=1)
test = test.drop(columns=['id'], axis=1)

train_data, test_data = train_test_split(train, random_state=911, stratify=train['label'])
trainX = train_data['tweet']
trainY = train_data['label']
testX = test_data['tweet']
testY = test_data['label']

clf = kNN_Texts(vectorizer_class = CountVectorizer, K=9,
                metric = Metric.EUCLIDEAN_DISTANCE #change here to see bonus work
                )

clf.fit(testX[:100], testY[:100])
pred = clf.predict(testX[:100]) 

tn, fp, fn, tp = confusion_matrix(testY[:100], pred).ravel()
print('TN: ', tn, 'FP: ', fp, 'FN: ', fn, 'TP: ', tp)
print(classification_report(testY[:100], pred))

clf = kNN_Texts(vectorizer_class=TfidfVectorizer, K=9,
                metric=Metric.EUCLIDEAN_DISTANCE #change here to see bonus work
                )

clf.fit(testX[:100], testY[:100])
pred = clf.predict(testX[:100])

tn, fp, fn, tp = confusion_matrix(testY[:100], pred).ravel()
print('TN: ', tn, 'FP: ', fp, 'FN: ', fn, 'TP: ', tp)

print(classification_report(testY[:100], pred))