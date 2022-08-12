# from sklearn.model_selection import train_test_split, KFold, cross_val_score, cross_val_predict, StratifiedKFold, GridSearchCV
# from numpy import mean, absolute, sqrt
# from sklearn.ensemble import RandomForestRegressor
import pandas as pd
# from sklearn.metrics import mean_absolute_error, mean_squared_error, accuracy_score
# from matplotlib import pyplot
# import numpy as np
# import seaborn as sns
# from sklearn.svm import SVR
# import matplotlib.pyplot as plt
# from sklearn import metrics, model_selection
# from sklearn.metrics import classification_report, confusion_matrix, fbeta_score, make_scorer, SCORERS
# from sklearn.preprocessing import StandardScaler, Normalizer, MinMaxScaler
# from sklearn.metrics import mean_squared_error
# from sklearn.preprocessing import OneHotEncoder
from joblib import load
import numpy as np

rnd = load('accounts/rnd_demand.joblib')


# train_set = pd.read_excel('dataframe.xlsx')
df= pd.read_excel('accounts/veriseti.xlsx')

df_year = df[(df["year"] == 2021) | (df["year"] == 2020)]
# df_year = df[(df["year"] == 2021)]
# print(df_year["year"])
onehot = df_year[["bolum", "fakulte", "universite", "burs","sehir", "dil"]]
onehot_df = pd.get_dummies(onehot, prefix_sep="_")
other_df = df_year.iloc[:,6:]
other_df = pd.DataFrame(other_df).drop(['Oran'], axis=1)
X_pred = pd.concat([onehot_df, other_df], axis=1) 
X_pred = X_pred[(X_pred["year"] == 2021)]
y_pre = X_pred["demand"].values.reshape(-1,1)
X_pred = pd.DataFrame(X_pred).drop(['demand'], axis=1)
X_pred = pd.DataFrame(X_pred).drop(['year'], axis=1)

def predict_demand(depart, uni):
    # bolum = X_pred.loc[(X_pred["bolum_İç Mimarlık ve Çevre Tasarımı (50 İndirimli)"] == 1) & (X_pred['universite_İSTANBUL SABAHATTİN ZAİM ÜNİVERSİTESİ']== 1)]
    filter = X_pred.loc[(X_pred["bolum_"+ depart] == 1) & (X_pred['universite_'+ uni]== 1)]
    # print(filter.index)
    # print("--------281 demand---------")
    # print(X_pred.filter(items = [15392], axis=0)["bolum_İç Mimarlık ve Çevre Tasarımı (50 İndirimli)"])
    # print(X_pred.filter(items = [15392], axis=0)['universite_İSTANBUL SABAHATTİN ZAİM ÜNİVERSİTESİ'])
    # print(X_pred.filter(items = [15392], axis=0)['score_last'])
    y_itu_pred = rnd.predict(filter)
    pred_demand = np.round(y_itu_pred, 2)
    print(pred_demand)
    return (pred_demand)