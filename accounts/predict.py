import pandas as pd
from joblib import load
import numpy
import warnings
warnings.filterwarnings('ignore')

rnd = load('accounts/rnd.joblib')
rnd_enroll = load('accounts/rnd_enroll.joblib')

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

def predict_dolulukOrani(bolum_name, uni_name):
    bolum_name = bolum_name.replace('%','')
    print(bolum_name)
    print(uni_name)
    bolum = X.loc[(X["bolum_" +bolum_name] == 1) & (X['universite_'+uni_name]== 1)]
    print(bolum)
    # print(bolum.index)
    # print("-----------------")
    # print(X.filter(items = [15591], axis=0)["bolum_Yapay Zeka ve Veri Mühendisliği (İngilizce)"])
    # print(X.filter(items = [15591], axis=0)['universite_İSTANBUL TEKNİK ÜNİVERSİTESİ'])
    # print(X.filter(items = [15591], axis=0)['score_last'])
    y_itu_pred = rnd.predict(bolum)
    y_itu_pred = numpy.round(y_itu_pred, 2)
    print(y_itu_pred)
    return (y_itu_pred)

other_enroll = df_year.iloc[:,6:]
X_enroll = pd.concat([onehot_df, other_enroll], axis=1) #standardize
X_enroll = X_enroll[(X_enroll["year"] == 2021)]
y_enroll = X_enroll["enrollment"].values.reshape(-1,1)
X_enroll = pd.DataFrame(X_enroll).drop(['enrollment'], axis=1)
X_enroll = pd.DataFrame(X_enroll).drop(['year'], axis=1)

def predict_enrollment(fakulte, burs, kapasite ):
    filter = X_enroll.loc[(X_enroll["fakulte_"+ fakulte] == 1) & (X_enroll['burs_'+ burs]== 1)]
    filter.loc[:, ('capacity')] = kapasite
 
    predict_enroll = rnd_enroll.predict(filter)
    result = pd.DataFrame(columns = ['bolum', 'predict'])
    filter['predict_enroll'] = predict_enroll
    filter = filter.sort_values(by=['predict_enroll'], ascending=False)
    for i in filter.index:
        for col in filter.columns.tolist():
           if ("bolum_" in col) and filter.at[i,col] == 1:
              result = result.append({'bolum' : col, 'predict' : filter.at[i,'predict_enroll']}, ignore_index=True)
    return result