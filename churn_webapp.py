from itertools import count
from unicodedata import category
from charset_normalizer import detect
import streamlit as st
import datetime
import time

import pandas as pd
import numpy as np



import plotly as plt
import plotly.graph_objects as go
import plotly.figure_factory as ff
import plotly.express as px



import functools
from locale import D_FMT
from plotly.subplots import make_subplots


from pickletools import float8
from sqlite3 import DatabaseError
from statistics import multimode
import plotly.express as px
import plotly.figure_factory as ff
from plotly.offline import init_notebook_mode, iplot
import plotly.graph_objs as go
from plotly.graph_objs import *
from plotly.offline import init_notebook_mode, iplot
import altair as alt
from PIL import Image
from typing import List, Tuple
import requests


from sklearn.preprocessing import FunctionTransformer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier
from sklearn.preprocessing import OrdinalEncoder
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import MinMaxScaler
from sklearn.impute import SimpleImputer
from sklearn.metrics import roc_auc_score
from sklearn.preprocessing import StandardScaler, RobustScaler

import hydralit_components as hc

from itertools import count
from unicodedata import category
from charset_normalizer import detect
import hydralit_components as hc

from streamlit_option_menu import option_menu
import streamlit.components.v1 as html
import io
from pathlib import Path
import base64


import pandas_profiling
from streamlit_pandas_profiling import st_profile_report
from pandas_profiling import ProfileReport

from sklearn.impute import KNNImputer
from sklearn.preprocessing import OrdinalEncoder
from fancyimpute import KNN
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import RendererAgg
from matplotlib.figure import Figure
import statsmodels
from statsmodels.nonparametric.smoothers_lowess import lowess

_lock = RendererAgg.lock
plt.style.use('default')

# Initial page config

st.set_page_config(
     page_title='Restaurant App',
     layout="wide",
     page_icon= 'eat.png',
     initial_sidebar_state="expanded"
)

def img_to_bytes(img_path):
    #to encode an image into a string
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded

st.sidebar.markdown('''[<img src='data:image/png;base64,{}' class='img-fluid' width=300 height=170>](https://eatapp.co)'''.format(img_to_bytes('eat.png')), 
                    unsafe_allow_html=True)

#-------------------------------------
#--------------SIDEBAR----------------
#-------------------------------------

st.sidebar.header('All in One App')

with st.sidebar:
        company_name = st.text_input("Enter The Restaurant Name")

with st.sidebar: 
        fileupload = st.file_uploader("Upload a dataset", type = ("csv", "xlsx"))
        if fileupload is None:
                with hc.HyLoader('Now doing loading',hc.Loaders.pulse_bars,):
                    time.sleep(5)

        else:
                data = pd.read_csv(fileupload)
        

with st.sidebar: 
        fileuploadclean = st.file_uploader("Upload the cleaned file", type = ("csv", "xlsx"))
        if fileuploadclean is None:
                st.write("Upload a file")
        else:
                dataclean = pd.read_csv(fileuploadclean)
                st.write(f'The dataset {fileuploadclean.name} contains {dataclean.shape[0]} rows and {dataclean.shape[1]} columns.')  

#-------------------------------------
#--------------NAV BAR----------------
#-------------------------------------

menu_data = [
        {'id':'data_preperation',
    'icon':"",
    'label':"Data Preperation",
    },
    
    {'id':'Chun_Analysis',
    'icon':"",
    'label':"Churn Analysis",
    },

        {'id':'Prediction',
    'icon':"",
    'label':"Prediction",
    }]

over_theme = {'txc_inactive': 'white','menu_background':'green','txc_active':'white','option_active':'green'}

menu_id = hc.nav_bar(
    menu_definition=menu_data,
    override_theme=over_theme,
    home_name='Home',
    login_name='Contact Info',
    hide_streamlit_markers=False, 
    sticky_nav=True, #at the top or not
    sticky_mode = 'pinned', #jumpy or not-jumpy, but sticky or pinned
)
      

def missing_zero_values_table(df):
        zero_val = (df == 0.00).astype(int).sum(axis=0)
        mis_val = df.isnull().sum()
        mis_val_percent = 100 * df.isnull().sum() / len(df)
        mz_table = pd.concat([zero_val, mis_val, mis_val_percent], axis=1)
        mz_table = mz_table.rename(
        columns = {0 : 'Zero Values', 1 : 'Missing Values', 2 : '% of Total Values'})
        mz_table['Total Zero Missing Values'] = mz_table['Zero Values'] + mz_table['Missing Values']
        mz_table['% Total Zero Missing Values'] = 100 * mz_table['Total Zero Missing Values'] / len(df)
        mz_table['Data Type'] = df.dtypes
        mz_table = mz_table[
            mz_table.iloc[:,1] != 0].sort_values(
        '% of Total Values', ascending=False).round(1)
        return mz_table


if menu_id == "data_preparation":
        st.header("Data Preparation")
        if fileupload is not None:
                st.write(f'The dataset {fileupload.name} contains {data.shape[0]} rows and {data.shape[1]} columns.')

                #Data Types handling
        
        st.subheader("Data Types")
        if fileupload is not None: 
                if st.checkbox("Show Data Types"):
                        st.write(data.dtypes.astype(str))

                cat_cols = st.multiselect('Choose columns to be converted into float numerical columns', 
                options=[c for c in data.columns.values], 
                )

                if st.checkbox("Convert to float"):
                        data[cat_cols] = data[cat_cols].astype(np.float64)
                        st.write(data[cat_cols].dtypes.astype(str))

                num_cols = st.multiselect('Choose columns to be converted into categorical columns', 
                options=[c for c in data.select_dtypes(include=[int, float]).columns.values], 
                )

                if st.checkbox("Convert to category"):
                        data[num_cols]= data[num_cols].astype('category')
                        st.write(data[num_cols].dtypes.astype(str))


                #Data Cleaning

                st.subheader("Missing Values")
                
                if st.checkbox("Show Missing Values"):
                        st.dataframe(missing_zero_values_table(data).astype(str))
                
                col1, col2 =st.columns(2)
                with col1:
                          st.subheader("Numerical Variables Missing Values")
                          numeric_cols = st.multiselect("Select numeric columns to treat", options=[c for c in data.select_dtypes(include=[int, float]).columns.values] )
                          #Methods to treat missing values
                          if len(numeric_cols)>0:
                                missing_value_method = st.selectbox("Select Missing Values Handling Technique", ("Remove","Replace with Median", "Replace with Mean","Replace with Mode"))
                                if missing_value_method == "Replace with Median":
                                        for column in data[numeric_cols].columns:
                                                data[column].fillna(data[column].median(), inplace=True)
                                        #Check if the missing values were removed
                                                #if st.checkbox("Show Numerical Missing Values After Treatment"):
                                        st.write(f'Results after treating {numeric_cols} using {missing_value_method}')
                                        st.write(data[numeric_cols].isnull().sum())

                                elif missing_value_method == "Replace with Mean":
                                        for column in data[numeric_cols].columns:
                                                data[column].fillna(data[column].mean(), inplace=True)
                                        #Check if the missing values were removed
                                        st.write(f'Results after treating {numeric_cols} using {missing_value_method}')
                                        st.write(data[numeric_cols].isnull().sum())

                                elif missing_value_method == "Replace with Mode":
                                        for column in data[numeric_cols].columns:
                                                data[column].fillna(data[column].mode()[0], inplace=True)
                                        #Check if the missing values were removed
                                        st.write(f'Results after treating {numeric_cols} using {missing_value_method}')
                                        st.write(data[numeric_cols].isnull().sum())
                                
                                else :
                                        for column in data[numeric_cols].columns:
                                                data= data.dropna( how='any',subset=[column])
                                        #Check if the missing values were removed
                                        st.write(f'Results after treating {numeric_cols} using {missing_value_method}')
                                        st.write(data[numeric_cols].isnull().sum())
             
                with col2:
                        st.subheader("Categorical Variables Missing Values")
                        cat_cols = st.multiselect("Select categorical columns to treat", options=[c for c in data.select_dtypes(exclude=[int, float]).columns.values] )
                        #Methods to treat missing value
                        if len(cat_cols)>0:
                                missing_value_method = st.selectbox("Select Missing Values Handling Technique", ("Replace with Mode", "KNN Imputer Coming Soon.."))
                                if missing_value_method == "Replace with Mode":
                                        for column in data[cat_cols].columns:
                                               data[column].fillna(data[column].mode()[0], inplace=True)
                                        #Check if the missing values were removed
                                        st.write(f'Results after treating {cat_cols} using {missing_value_method}')
                                        st.write(data[cat_cols].isnull().sum())

                #Duplicates 

                st.subheader("Duplicates")
                st.write(f'There are {data.duplicated().sum()} duplicates in the dataset.')
                if st.checkbox("Remove Duplicates"):
                        data = data.drop_duplicates()
                        st.write(f'{data.duplicated().sum()} duplicates are left')
                
                st.header("Outliers")
                def remove_outlier(df_in, col_name):
                        q1 = df_in[col_name].quantile(0.25)
                        q3 = df_in[col_name].quantile(0.75)
                        iqr = q3-q1 #Interquartile range
                        fence_low  = q1-1.5*iqr
                        fence_high = q3+1.5*iqr
                        df_in = df_in.loc[(df_in[col_name] > fence_low) & (df_in[col_name] < fence_high)]
                        return df_in
                num_cols = st.selectbox('Choose a numerical column to remove outliers', 
                options=[c for c in data.select_dtypes(include=[int, float]).columns.values], 
                )
                if st.checkbox("Remove Outliers"):
                        remove_outlier(data, num_cols)
                
                #Download Cleaned dataset

                st.write(f'The dataset {fileupload.name} contains {data.shape[0]} rows and {data.shape[1]} columns.')

                @st.cache
                def convert_df(df):
                        return df.to_csv().encode('utf-8')


                csv = convert_df(data)

                st.download_button(
                        "Press to Download The Cleaned Dataset",
                        csv,
                        f"{company_name}_dfupdated.csv",
                        "text/csv",
                        key='download-csv'
                        )

#------------------------------------------
#------------Churn Dashboard------------
#------------------------------------------
if menu_id == "Chun_Analysis":
        st.header("Churn Analytics Dashboard")
        if fileuploadclean is not None:

                st.header("Churn Analytics Dashboard")

                from streamlit_lottie import st_lottie
                import json


                def load_lottiefile(filepath: str):
                        with open(filepath, "r") as f:
                                return json.load(f)

                df = dataclean




                df1= df.groupby(['Churn', 'Package']).size().reset_index(name='counts')
                df1 = pd.pivot_table(df1, values=['counts'], columns=None, index=['Package'], aggfunc='sum', sort=True)
                df1 = df1.reset_index()
                sorted1 = df1.sort_values(by='counts', ascending=False).reset_index()



                df2= df.groupby(['Churn', 'Lifecycle']).size().reset_index(name='counts')
                df2 = pd.pivot_table(df2, values=['counts'], columns=None, index=['Lifecycle'], aggfunc='sum')
                df2 = df2.reset_index()
                sorted2 = df2.sort_values(by='counts', ascending=False).reset_index()

                df3= df.groupby(['Churn', 'Billing Cycle']).size().reset_index(name='counts')
                df3 = pd.pivot_table(df3, values=['counts'], columns=None, index=['Billing Cycle'], aggfunc='sum')
                df3 = df3.reset_index()
                sorted3 = df3.sort_values(by='counts', ascending=False).reset_index()

                df4= df.groupby(['Churn', 'warning']).size().reset_index(name='counts')
                df4 = pd.pivot_table(df4, values=['counts'], columns=None, index=['warning'], aggfunc='sum',sort=True)
                df4 = df4.reset_index()
                sorted4 = df4.sort_values(by='counts', ascending=False).reset_index()

                df5 = df.groupby(['Churn', 'Region']).size().reset_index(name='counts')
                df5 = pd.pivot_table(df5, values=['counts'], columns=None, index=['Region'], aggfunc='sum', sort=True)
                df5 = df5.reset_index()
                sorted5 = df5.sort_values(by='counts', ascending=False).reset_index()


                df6 = df.groupby(['Churn', 'actual_covers']).size().reset_index(name='counts')
                df6 = pd.pivot_table(df6, values=['counts'], columns=None, index=['actual_covers'], aggfunc='sum', sort=True)
                df6 = df6.reset_index()
                sorted6 = df6.sort_values(by='counts', ascending=False).reset_index()



                #line dividing animations with plots
                theme_override = {'bgcolor': 'rgb(51,160,44)','title_color': 'white','content_color': 'white','progress_color': 'rgb(51,160,44)',
                'icon_color': 'white', 'icon': 'bi bi-calendar', 'content_text_size' : '50%'}
                hc.progress_bar(content_text= 'Demographics', override_theme=theme_override)


                churn = list(df.Churn.unique())
                churn_filter = st.selectbox("Churn", churn)
                df = df[df["Churn"] == churn_filter]

                #splitting again for plots
                #col12, col22= st.columns(2)

                churn1, churn2, churn3 =st.columns(3)

                with churn1:

                        df1= df.groupby(['Churn', 'Package']).size().reset_index(name='counts')
                        df1 = pd.pivot_table(df1, values=['counts'], columns=None, index=['Package'], aggfunc='sum', sort=True)
                        df1 = df1.reset_index()
                        churn1 = go.Figure(px.treemap(df1, path=['Package'], values='counts',
                                color_discrete_sequence= ['rgb(178,223,138)', 'rgb(31,120,180)', 'rgb(51,160,44)', ' rgb(166,206,227)',
                                'rgb(50,205,50)', 'rgb(0,128,0)'],
                        labels= {'Churn': 'Churn Score',
                                'counts':'Number of Customers'}
                                ))
                        churn1.update_layout(xaxis=dict(showgrid=False), yaxis=dict(showgrid=False), width=600,
                                title='Package Groups',
                                title_font_size=24)
                        churn1.update_layout({ 'plot_bgcolor': 'rgba(0, 0, 0, 0)', 'paper_bgcolor': 'rgba(0, 0, 0, 0)'})
                        st.plotly_chart(churn1)
                        st.caption(f"""
                                <div>
                                <div style="vertical-align:left;font-size:16px;padding-left:5px;padding-top:5px;margin-left:0em";>
                                The most used package by customers is {sorted1['Package'].loc[0]}
                                </div>""",unsafe_allow_html = True)

                st.empty()
                st.write('')
                st.write('')
                st.write('')

                #divide to seperate sections
                theme_override = {'bgcolor': 'rgb(51,160,44)','title_color': 'white','content_color': 'white','progress_color': 'rgb(51,160,44)',
                }
                hc.progress_bar(content_text= 'Options Available', override_theme=theme_override)

                #plot2

                with churn2: 

                        df3= df.groupby(['Churn', 'Billing Cycle']).size().reset_index(name='counts')
                        df3 = pd.pivot_table(df3, values=['counts'], columns=None, index=['Billing Cycle'], aggfunc='sum', sort=True)
                        df3 = df3.reset_index()
                        churn2 = go.Figure(px.pie(df3, values='counts', names='Billing Cycle',
                                color_discrete_sequence= ['rgb(178,223,138)', 'rgb(31,120,180)'],
                                labels= {'Billing Cycle': 'Billing Cycle',
                                         'counts':'Number of Customers'}
                                ))
                        churn2.update_layout(xaxis=dict(showgrid=False), yaxis=dict(showgrid=False), width=500,
                                        title='Billing Cycle Distribution',
                                        title_font_size=24)
                        churn2.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)', 'paper_bgcolor': 'rgba(0, 0, 0, 0)'})
                        st.plotly_chart(churn2)

                with churn3:

                        df4 = df.groupby(['Churn', 'warning']).size().reset_index(name='counts')
                        df4['Churn'] = df4['Churn'].astype(str)
                        churn3 = go.Figure(px.histogram(df4, x='warning', y='counts',barmode='group',
                                color_discrete_sequence= ['rgb(31,120,180)'],
                                labels= {'counts':'Number of Customers',
                                        'warning': 'warning'}))
                        churn3.update_layout(xaxis=dict(showgrid=False), yaxis=dict(showgrid=False), width=600,
                                title='warning',
                                title_font_size=24)
                        churn3.update_layout({ 'plot_bgcolor': 'rgba(0, 0, 0, 0)', 'paper_bgcolor': 'rgba(0, 0, 0, 0)'})
                        st.plotly_chart(churn3)

                churn4, churn5 =st.columns(2)

                #plot4
                with churn4:

                        df2= df.groupby(['Churn', 'Lifecycle']).size().reset_index(name='counts')
                        churn4 = go.Figure(px.histogram(df2, x='Lifecycle', y='counts', barmode='group',
                                color_discrete_sequence= ['rgb(178,223,138)'],
                                labels= {'Lifecycle': 'Lifecycle',
                                        'counts':'Number of Customers'}))
                        churn4.update_layout(xaxis=dict(showgrid=False), yaxis=dict(showgrid=False), width=600,
                                title='Lifecycle',
                                title_font_size=24)
                        churn4.update_layout({ 'plot_bgcolor': 'rgba(0, 0, 0, 0)', 'paper_bgcolor': 'rgba(0, 0, 0, 0)'})
                        st.plotly_chart(churn4)
                        st.caption(f"""
                                <div>
                                <div style="vertical-align:left;font-size:16px;padding-left:5px;padding-top:5px;margin-left:0em";>
                                Most  customers churn after subscription for   days
                                </div>""",unsafe_allow_html = True)



                ######################################################################################################################
                # Creating the Time Series Analysis Page

                # Creating the Time Series Plots
                from matplotlib.pyplot import subplots
                import plotly.subplots as subplots

                # Bookings time Series

                with churn5:
                        churn5 = subplots.make_subplots(rows=2, 
                                        cols=1, 
                                        subplot_titles=('Count of Bookings'
                                                ))

                        custom_aggregation = {}
                        custom_aggregation["Last_Reservation"] = "count"
                        df = df.set_index(pd.DatetimeIndex(df['Last_Reservation']))
                        data2 = df.resample('W').agg(custom_aggregation)
                        data2.columns = ["actual_covers"]
                        data2['year'] = data2.index

                        x = data2['year'].tolist()
                        y = data2['actual_covers'].tolist()

                        churn5.add_trace(go.Scatter(x=x, y=y,line=dict(color='green', width=4)), 1, 1)

                        churn5['layout'].update(height=700, width=800, title='Booking Time Series')

                        churn5.update_layout(title='Booking Time Series',
                        xaxis_title='Month',
                        yaxis_title='booking',xaxis=dict(showgrid=False), yaxis=dict(showgrid=False),plot_bgcolor="white")



                        st.plotly_chart(churn5)



if menu_id=="Prediction":

        df = dataclean
        
        import datetime
        from datetime import datetime, date

        from datetime import timedelta

        df['Last_Reservation'] = pd.to_datetime(df['Last_Reservation'])
        df['End Date'] = pd.to_datetime(df['End Date'])
        df['Start Date'] = pd.to_datetime(df['Start Date'])
        df['Last_Reservation'].dt.to_period('M')
        df['End Date'].dt.to_period('M')
        df['month'] = pd.to_datetime(df['Start Date']).dt.month


                #seperate title and animation
        col1, col2= st.columns([2,2])
        with col1:
                st.title("Your Turn to Predict!")
                st.write("Fill out your customers' information and get their Churn Risk Score")
                st.caption(f"""
                <div>
                <div style="vertical-align:left;font-size:16px;padding-left:5px;padding-top:5px;margin-left:0em";>
                Examine whether your customer would have a high or low churn risk score through his behavior, demographics, and feedback. These are all key factors in predicting whether the customer would leave. To build efficient marketing campaigns and decrease uneccessary costs, it is crucial to examine this score for future customers.
                </div>""",unsafe_allow_html = True)


        with col2:
                st.write("predict")
                #animation13
                #lottie_app= load_lottiefile("application.json")
                #st_lottie(lottie_app, height=360, width=550)
        
        st.empty()

        theme_override = {'bgcolor': 'rgb(51,160,44) ','title_color': 'white','content_color': 'white','progress_color': ' rgb(51,160,44)'}
        hc.progress_bar(content_text= 'Fill the Form', override_theme=theme_override)

        numerical_features = ['actual_covers', 'Lifecycle', 'Adjusted Price']
        df_numerical = df[numerical_features]
        categorical_features =['Billing Cycle', 'Package', 'Group','Region', 'warning']
        df_categorical = df[categorical_features]
        
        # Features
        X = pd.concat([df_categorical, df_numerical], axis = 1)

        y = df['Churn']

            #defining function to create inputs that will give a prediction
        def user_input_features():

                col3, col4= st.columns(2)
                with col3:
                        actual_covers = st.number_input("Insert the number of covers of the customer", value=1, min_value=0)
                        Lifecycle = st.number_input('Insert the Number of days since the customer used the system', value=1, min_value=1)
                        Adjusted_Price = st.number_input("Insert the Price  spent by the customer", value=1, min_value=1)       
                        Billing_Cycle= st.selectbox('Select the billing of the customer', ('annual', 'biannual','monthly','quarterly'))
                
                with col4:         
                        Package= st.selectbox('Select the Package of the customer', ('automation_feature', 'marketing_pro', 'pay_per_cover','pay_per_sms','phone_integration','pos_upgrade','table_management'))
                        Group= st.selectbox('Select if the restaurant is in a group', ('YES', 'NO'))
                        Region= st.selectbox('Select the Region of the customer', ('Global', 'Jeddah', 'Kuwait','Muscat','Nothern Emirates','Riyadh','United Kingdom','United States',' Dubai'))
                        warning= st.selectbox('warning of the customer', ('TRUE', 'FALSE'))

                        data = {'actual_covers': actual_covers, 'Lifecycle': Lifecycle, 'Adjusted Price': Adjusted_Price,'Billing Cycle': Billing_Cycle, 'Package': Package, 'Group': Group, 'Region':Region, 'warning': warning}

                features= pd.DataFrame(data, index=[0])
                return features

        df1= user_input_features()

        #encoding categorical variable
        encoderlabel = LabelEncoder()
        y = encoderlabel.fit_transform(y)

        #pipeline for all necessary transformations
        cat_pipeline= Pipeline(steps=[
                ('impute', SimpleImputer(missing_values = np.nan, strategy = 'constant', fill_value = 'None')),
                ('ohe', OneHotEncoder(handle_unknown = 'ignore'))
                ])

        num_pipeline = Pipeline(steps=[

                ('impute', SimpleImputer(missing_values = np.nan, strategy='mean')),
                ('outlier',RobustScaler())
                ])

        column_transformer= ColumnTransformer(transformers=[
                ('ohe', cat_pipeline, categorical_features),
                ('impute', num_pipeline, numerical_features)
                ], remainder='drop')

        #chose best model based on previous trials
        model = RandomForestClassifier(class_weight='balanced')

        pipeline_model = Pipeline(steps = [('transformer', column_transformer),
                                ('model', model)])

        #train the model
        pipeline_model.fit(X, y)

           #predicting the data
        prediction = pipeline_model.predict(df1)

        m = st.markdown("""
         <style>
                 div.stButton > button:first-child {
                color: #fff;
                background-color: rgb(51,160,44);
                }
                </style>""", unsafe_allow_html=True)
        submit = st.button('Predict')

        if submit:
                st.subheader(f'The Churn Risk Score of the customer is {str(prediction)}')
                st.write('---')
