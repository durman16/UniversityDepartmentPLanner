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
import numpy

rnd = load('accounts/rnd.joblib')


# train_set = pd.read_excel('dataframe.xlsx')
df= pd.read_excel('accounts/veriseti.xlsx')

df_year = df[(df["year"] == 2021) | (df["year"] == 2020)]
# df_year = df[(df["year"] == 2021)]
# print(df_year["year"])
onehot = df_year[["bolum", "fakulte", "universite", "burs","sehir", "dil"]]
onehot_df = pd.get_dummies(onehot, prefix_sep="_")
# df_year = df_year[(df_year["year"] == 2021)]
# train_set.loc[:, "Oran"] = train_set["Oran"].map('{:.3f}'.format)
other_df = df_year.iloc[:,6:]
# other_df = pd.DataFrame(other_df).drop(['year'], axis=1)
other_df = pd.DataFrame(other_df).drop(['enrollment'], axis=1)
other_df = pd.DataFrame(other_df).drop(['capacity'], axis=1)
# other_df = pd.DataFrame(other_df).drop(['Oran'], axis=1)
other_df[other_df.columns] = other_df[other_df.columns].apply(pd.to_numeric, errors='ignore')
X = pd.concat([onehot_df, other_df], axis=1) #standardize
X = X[(X["year"] == 2021)]
y = X["Oran"].values.reshape(-1,1)
X = pd.DataFrame(X).drop(['Oran'], axis=1)
X = pd.DataFrame(X).drop(['year'], axis=1)

def predict(bolum_name, uni_name):
    bolum_name = bolum_name.replace('%','')
    print(bolum_name)
    print(uni_name)
    bolum = X.loc[(X["bolum_" +bolum_name] == 1) & (X['universite_'+uni_name]== 1)]
    # print(bolum.index)
    # print("-----------------")
    # print(X.filter(items = [15591], axis=0)["bolum_Yapay Zeka ve Veri Mühendisliği (İngilizce)"])
    # print(X.filter(items = [15591], axis=0)['universite_İSTANBUL TEKNİK ÜNİVERSİTESİ'])
    # print(X.filter(items = [15591], axis=0)['score_last'])
    y_itu_pred = rnd.predict(bolum)
    y_itu_pred = numpy.round(y_itu_pred, 2)
    print(y_itu_pred)
    return (y_itu_pred)
