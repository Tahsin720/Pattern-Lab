# -*- coding: utf-8 -*-
"""Assignment_1(NB).ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/13hUP8vJ5_rDBBoTOhSh_l3k1fRicgSJO
"""

import numpy as np
import pandas as pd

df = pd.read_csv("/content/drive/MyDrive/Colab Notebooks/Assignment_1/WA_Fn-UseC_-Telco-Customer-Churn.csv",
                 na_values=["No internet service", "No phone service"])

df.dropna()
df.dropna(inplace=True)
df.reset_index(drop=True)

df.drop(labels=["Partner", "customerID"], 
          axis=1,
          inplace=True
        )

df = df.replace({
    "Churn": {
        "Yes": 1,
        "No": 0
    }
})

# Divide dataset into two parts
numerical_columns = pd.DataFrame(df, 
                        columns = ["SeniorCitizen", "tenure", "MonthlyCharges", "TotalCharges"])
categorical_columns = pd.DataFrame(df, 
                        columns = ["gender", "Dependents", "PhoneService", "MultipleLines", "InternetService", "OnlineSecurity", "OnlineBackup", "DeviceProtection", "TechSupport", "StreamingTV", "StreamingMovies", "Contract",	"PaperlessBilling", "PaymentMethod"])

numerical_columns.dropna()
categorical_columns.dropna()

print(numerical_columns)
print(categorical_columns)

data_x = categorical_columns.loc[:, categorical_columns.columns != "Churn"]
data_y = df["Churn"]

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(data_x, data_y, train_size = 0.8, random_state = 911)
X_train_st, X_test_st, y_train_st, y_test_st = train_test_split(data_x, data_y, train_size = 0.8, stratify = data_y, random_state = 911)
print(X_train.shape)

# accu = np.sum(np.equal(test_y, preds))/len(test_y)
# print(f'accuracy={accu}')

def acc_rate(prediction, test_y):
  test_y = np.array(test_y)
  count = 0
  for i in range(len(prediction)):
    if prediction[i] == test_y[i]:
      count += 1
  # print(count)
  return(count / len(test_y))

#without library
def matrix(prediction, y_test):
  tn = 0 
  fp = 0 
  fn = 0 
  tp = 0
  y_test = np.array(y_test)
  for i in range(len(prediction)):
    if y_test[i] == prediction[i] == 1:
      tp += 1
    elif prediction[i] == 1 and y_test[i] != prediction[i]:
      fp += 1
    elif y_test[i] == y_test[i] == 0:
      tn += 1
    elif prediction[i] == 0 and y_test[i] != prediction[i]:
      fn += 1
  return(tn, fp, fn, tp)

label_class = []
dictionary = {}

def fit(X_train, y_train):
    y_train = np.array(y_train)
    X_train = np.array(X_train)
    dictionary.clear()
    label_class.clear()
    for i in range(np.max(y_train) + 1):
        label_class.append(list(y_train).count(i)/len(y_train))
    
    for i in range(X_train.shape[1]):
        curr_feature_value = X_train[:,i]
        for j in range(len(curr_feature_value)):
            if (i, curr_feature_value[j], y_train[j]) in dictionary:
                dictionary[(i,curr_feature_value[j],y_train[j])] += (1/list(y_train).count(y_train[j]))
            else:
                dictionary[(i,curr_feature_value[j],y_train[j])] = (1/list(y_train).count(y_train[j]))
    return dictionary


def predict(X_test, dictionary):
    learn_values = []
    X_test = np.array(X_test)

    for arr_test in X_test:
        temp_value = 0
        pred_value = 0
        for i in range(len(label_class)):
            store = label_class[i]
            for j in range(len(arr_test)):
                store = store * dictionary[(j, arr_test[j], i)]
            if store > temp_value:
                temp_value = store
                pred_value = i
        learn_values.append(pred_value)
    return learn_values

#without applying stratification

from sklearn.metrics import recall_score, precision_score, accuracy_score, f1_score

dic = fit(X_train, y_train)

prediction = predict(X_test, dic)  

accuracy = accuracy_score(y_test, prediction)
# print(accuracy)
precision = precision_score(y_test, prediction)
recall = recall_score(y_test, prediction)
f1_sc = f1_score(y_test, prediction)

print("Accuracy: " , accuracy , " " , "Precision: " , precision , " " , "Recall: " , recall , " " , "f1_score: " , f1_sc)

# Applying stratification

dic1 = fit(X_train_st, y_train_st)
prediction1 = predict(X_test_st, dic1)

accuracy = accuracy_score(y_test_st, prediction1)
# print(accuracy)
precision = precision_score(y_test_st, prediction1)
recall = recall_score(y_test_st, prediction1)
f1_sc = f1_score(y_test_st, prediction1)

print("Accuracy: " , accuracy , " " , "Precision: " , precision , " " , "Recall: " , recall , " " , "f1_score: " , f1_sc)

#using libray for 1st dictionary without stratification
from sklearn.metrics import confusion_matrix
tn, fp, fn, tp = confusion_matrix(y_test, prediction).ravel()
print(tn, fp, fn, tp)

#using libray for 2nd dictionary wit stratification
tn, fp, fn, tp = confusion_matrix(y_test, prediction1).ravel()
print(tn, fp, fn, tp)

#Without stratification output using my code

accuracy = acc_rate(prediction, y_test)

tn, fp, fn, tp = matrix(prediction, y_test)
print(tn, fp, fn, tp)

precision = (tp/(tp+fp))
recall = (tp/(tp+fn))
f1_sc = 2*((precision * recall)/(precision + recall))

print("Accuracy: " , accuracy , " " , "Precision: ", precision, "Recall: ", recall, " " , "f1_score: " , f1_sc)

#With stratification output using my code

accuracy = acc_rate(prediction1, y_test_st)

tn, fp, fn, tp = matrix(prediction1, y_test_st)
print(tn, fp, fn, tp)

precision = (tp/(tp+fp))
recall = (tp/(tp+fn))
f1_sc = 2*((precision * recall)/(precision + recall))

print("Accuracy: " , accuracy , " " , "Precision: ", precision, "Recall: ", recall, " " , "f1_score: " , f1_sc)