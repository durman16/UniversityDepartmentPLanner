import pandas as pd
from joblib import load
import numpy
import warnings
warnings.filterwarnings('ignore')

rnd = load('accounts/ml_model/rnd.joblib')
rnd_enroll = load('accounts/ml_model/rnd_enroll.joblib')
rnd_point = load('accounts/ml_model/rnd_point2.joblib')
tree_capa = load('accounts/ml_model/tree_capacity.joblib')

# train_set = pd.read_excel('dataframe.xlsx')
df= pd.read_excel('accounts/data/veriseti.xlsx')

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

def enrollment_2c(universite, fakulte, bolum ):
    filter = X_enroll.loc[(X_enroll["universite_"+ universite] == 1) & (X_enroll['bolum_'+ bolum]== 1)]
    predict_enroll = rnd_enroll.predict(filter)
    return predict_enroll

point_other = df_year.iloc[:,6:]
# other_df = pd.DataFrame(other_df).drop(['year'], axis=1)
# other_df = pd.DataFrame(other_df).drop(['enrollment'], axis=1)
# other_df = pd.DataFrame(other_df).drop(['capacity'], axis=1)
X_pred = pd.concat([onehot_df, point_other], axis=1) #standardize
# ehe = X_pred.loc[(X_pred["bolum_İç Mimarlık ve Çevre Tasarımı (50 İndirimli)"] == 1) & (X_pred['universite_İSTANBUL SABAHATTİN ZAİM ÜNİVERSİTESİ']== 1)]
X_pred = X_pred[(X_pred["year"] == 2021)]
y_predict = X_pred["score_last"].values.reshape(-1,1)
# print(np.array(y_pre).index(15392))
# print(other_df.dtypes)
# other_df[other_df.columns] = other_df[other_df.columns].apply(pd.to_numeric, errors='ignore')
X_pred = pd.DataFrame(X_pred).drop(['score_last'], axis=1)
X_pred = pd.DataFrame(X_pred).drop(['year'], axis=1)

def predict_point(fakulte, burs, kapasite ):
    # bolum = X_pred.loc[(X_pred["bolum_İç Mimarlık ve Çevre Tasarımı (50 İndirimli)"] == 1) & (X_pred['universite_İSTANBUL SABAHATTİN ZAİM ÜNİVERSİTESİ']== 1)]
    filter = X_pred.loc[(X_pred["fakulte_"+ fakulte] == 1)  &(X_pred['burs_'+ burs]== 1)]
    filter.loc[:, ('capacity')] = kapasite
    predict_point = rnd_point.predict(filter)
    result = pd.DataFrame(columns = ['bolum', 'predict'])
    filter['predict_point'] = predict_point
    filter = filter.sort_values(by=['predict_point'], ascending=False)
    for i in filter.index:
        for col in filter.columns.tolist():
           if ("bolum_" in col) and filter.at[i,col] == 1:
              result = result.append({'bolum' : col, 'predict' : filter.at[i,'predict_point']}, ignore_index=True)
    return result

def b2_enrollment(fakulte, bolum, kapasite ):
    # bolum = X_pred.loc[(X_pred["bolum_İç Mimarlık ve Çevre Tasarımı (50 İndirimli)"] == 1) & (X_pred['universite_İSTANBUL SABAHATTİN ZAİM ÜNİVERSİTESİ']== 1)]
    filter = X_enroll.loc[(X_pred["fakulte_"+ fakulte] == 1) & (X_enroll['bolum_'+ bolum]== 1)]
    filter.loc[:, ('capacity')] = kapasite
    predict_enroll = rnd_enroll.predict(filter)
    filter['predict_enroll'] = predict_enroll
    result = filter['predict_enroll'].mean()
    return result

def b2_point(fakulte, bolum, kapasite ):
        # bolum = X_pred.loc[(X_pred["bolum_İç Mimarlık ve Çevre Tasarımı (50 İndirimli)"] == 1) & (X_pred['universite_İSTANBUL SABAHATTİN ZAİM ÜNİVERSİTESİ']== 1)]
        filter = X_pred.loc[(X_pred["fakulte_"+ fakulte] == 1) & (X_pred['bolum_'+ bolum]== 1)]
        filter.loc[:, ('capacity')] = kapasite
        predict_point = rnd_point.predict(filter)
        filter['predict_point'] = predict_point
        result = filter['predict_point'].mean()
        return result


other_capa = df_year.iloc[:,6:]
# other_df = pd.DataFrame(other_df).drop(['year'], axis=1)
# other_df = pd.DataFrame(other_df).drop(['enrollment'], axis=1)
# other_df = pd.DataFrame(other_df).drop(['capacity'], axis=1)
X_capa = pd.concat([onehot_df, other_capa], axis=1) #standardize
# ehe = X_pred.loc[(X_pred["bolum_İç Mimarlık ve Çevre Tasarımı (50 İndirimli)"] == 1) & (X_pred['universite_İSTANBUL SABAHATTİN ZAİM ÜNİVERSİTESİ']== 1)]
X_capa = X_capa[(X_capa["year"] == 2021)]
y_capa = X_capa["capacity"].values.reshape(-1,1)
# print(np.array(y_pre).index(15392))
# print(other_df.dtypes)
# other_df[other_df.columns] = other_df[other_df.columns].apply(pd.to_numeric, errors='ignore')
X_capa = pd.DataFrame(X_capa).drop(['capacity'], axis=1)
X_capa = pd.DataFrame(X_capa).drop(['enrollment'], axis=1)
X_capa = pd.DataFrame(X_capa).drop(['year'], axis=1)

def predict_capacity(uni, fakulte, bolum, min_base, oran ):
    # bolum = X_pred.loc[(X_pred["bolum_İç Mimarlık ve Çevre Tasarımı (50 İndirimli)"] == 1) & (X_pred['universite_İSTANBUL SABAHATTİN ZAİM ÜNİVERSİTESİ']== 1)]
    filter = X_capa.loc[(X_pred["fakulte_"+ fakulte] == 1) & (X_capa["universite_"+ uni] == 1) &(X_capa['bolum_'+ bolum]== 1)]
    filter.loc[:, ('score_last')] = min_base
    filter.loc[:, ('Oran')] = oran
    predict_capa = tree_capa.predict(filter)
    # filter['predict_capa'] = predict_capa
    # filter = filter.sort_values(by=['predict_capa'], ascending=False)
    return predict_capa