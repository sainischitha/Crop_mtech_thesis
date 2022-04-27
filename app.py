# Importing essential libraries and modules

from flask import Flask, render_template, request, Markup
import numpy as np
import pandas as pd
import requests
import config
import pickle
import io


# import StandardScaler to perform scaling
from sklearn.preprocessing import MinMaxScaler 

from sklearn.preprocessing import LabelEncoder


# ==============================================================================================

# -------------------------LOADING THE TRAINED MODELS -----------------------------------------------

# Loading plant disease classification model



crop_recommendation_model_path = 'models/model_lgb.pkl'
crop_recommendation_model = pickle.load(
    open(crop_recommendation_model_path, 'rb'))

crop_damage_model_path = 'models/model_lightgbm_cd.pkl'
crop_damage_model = pickle.load(
    open(crop_damage_model_path, 'rb'))


# =========================================================================================

# Custom functions for calculations


# ===============================================================================================
# ------------------------------------ FLASK APP -------------------------------------------------


app = Flask(__name__)

# render home page


@ app.route('/')
def home():
    title = 'FarmRemedy - Home'
    return render_template('index.html', title=title)

# render crop recommendation form page


@ app.route('/crop-recommend')
def crop_recommend():
    title = 'FarmRemedy - Crop Recommendation'
    return render_template('crop.html', title=title)

# render fertilizer recommendation form page


@ app.route('/Crop-Damage-Detection')
def crop_damage():
    title = 'FarmRemedy - Crop Damage Classification'

    return render_template('fertilizer.html', title=title)

# render disease prediction input page




# ===============================================================================================

# RENDER PREDICTION PAGES

# render crop recommendation result page


@ app.route('/crop-predict', methods=['POST'])
def crop_prediction():
    title = 'FarmRemedy - Crop Recommendation'

    if request.method == 'POST':
        N = float(request.form['nitrogen'])
        P = float(request.form['phosphorous'])
        K = float(request.form['pottasium'])
        pH = float(request.form['ph'])
        rain = float(request.form['rainfall'])
        temp=float(request.form['temperature'])
        Area=float(request.form['area'])
        prod=float(request.form['production'])
        state = request.form.get("tst1")
        dis = request.form.get("tst2")
        season = request.form.get("tst")

        df = pd.read_csv('crops_final.csv')

        df.drop(['Crop_Year','Sowing Temp','Harvest Temp'],axis=1,inplace=True)
        df.dropna(inplace=True)
        df.reset_index(drop=True,inplace=True)

        df_num_features=df.select_dtypes(include=np.number)
        Q1 = df_num_features.quantile(0.25)
        Q3 = df_num_features.quantile(0.75)
        IQR = Q3 - Q1
        df_out = df[~((df < (Q1 - 1.75 * IQR)) |(df > (Q3 + 1.75 * IQR))).any(axis=1)]
        df_out.reset_index(inplace=True,drop=True)

        df_num=df_out.select_dtypes(include=np.number)

        num_arr=pd.DataFrame(np.array([[Area,prod,temp,pH,rain,P,N, K]]),columns=df_num.columns)
        num_data=pd.concat([df_num,num_arr],axis=0)
        num_data.reset_index(drop=True,inplace=True)

        df_cat=df_out.select_dtypes(include='object')
        df_cat.drop('crop',axis=1,inplace=True)

        cat_arr=pd.DataFrame([[state,dis,season]],columns=df_cat.columns)
        cat_data=pd.concat([df_cat,cat_arr],axis=0)
        cat_data.reset_index(drop=True,inplace=True)

        df_en=pd.get_dummies(cat_data['Season'],drop_first=True)
        df_ssn=pd.get_dummies(cat_data['State_Name'],drop_first=True)
        le=LabelEncoder()
        df_dn=pd.DataFrame(le.fit_transform(cat_data['District_Name']),columns=['District_Name'])

        df_categorical = pd.concat([df_ssn,df_en,df_dn],axis=1)

        mms = MinMaxScaler()
        df_mms = pd.DataFrame(mms.fit_transform(num_data), columns = num_data.columns)

        df_final = pd.concat([df_mms, df_categorical], axis = 1)

        df_last=df_final.iloc[-1,:]
        my_prediction = crop_recommendation_model.predict(np.array([df_last]))
        final_prediction = my_prediction

        return render_template('crop-result.html', prediction=final_prediction, title=title)

# render fertilizer recommendation result page


@ app.route('/fertilizer-predict', methods=['POST'])
def fert_recommend():
    title = 'FarmRemedy - Crop Damage Classification'
    
    if request.method == 'POST':
        eic= float(request.form['estimated Insects count'])
        ndw = float(request.form['number_doses_week'])
        nwu = float(request.form['number_week_used'])
        nwq = float(request.form['number_week_quit'])
        ct = request.form.get("ctt")
        st = request.form.get("styp")
        pus = request.form.get("put")
        seas = request.form.get("tstn")
    
        df = pd.read_csv('Crop_Damage.csv')
        df.drop('ID',axis=1,inplace=True)
        df['Crop_Damage']=df['Crop_Damage'].astype('object')
        df_num_features=df.select_dtypes(include=np.number)
        Q1 = df_num_features.quantile(0.25)
        Q3 = df_num_features.quantile(0.75)
        IQR = Q3 - Q1
        df_out = df[~((df < (Q1 - 1.5 * IQR)) |(df > (Q3 + 1.5 * IQR))).any(axis=1)]
        df_out.reset_index(inplace=True,drop=True)

        df_num=df_out.select_dtypes(include=np.number)
        num_arr=pd.DataFrame(np.array([[eic,ndw,nwu,nwq]]),columns=df_num.columns)
        num_data=pd.concat([df_num,num_arr],axis=0)
        num_data.reset_index(drop=True,inplace=True)

        df_cat=df_out.select_dtypes(include='object')
        df_cat.drop('Crop_Damage',axis=1,inplace=True)

        cat_arr=pd.DataFrame([[ct,st,pus,seas]],columns=df_cat.columns)
        cat_data=pd.concat([df_cat,cat_arr],axis=0)
        cat_data.reset_index(drop=True,inplace=True)

        df_en=pd.get_dummies(cat_data)

        mms = MinMaxScaler()
        df_mms = pd.DataFrame(mms.fit_transform(num_data), columns = num_data.columns)

        df_final = pd.concat([df_mms,df_en], axis = 1)

        df_last=df_final.iloc[-1,:]
        my_prediction = crop_damage_model.predict(np.array([df_last]))
        
        if my_prediction == 0:
            final_prediction='alive'
        elif my_prediction == 1:
            final_prediction='damaged due to other causes'
        else:
            final_prediction ='damaged due to Pesticides'
        
        return render_template('fertilizer-result.html', prediction=final_prediction, title=title)

# ===============================================================================================
if __name__ == '__main__':
    app.run(debug=False)
