# -*- coding: utf-8 -*-
"""DAG_Final.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1AG752sksil_cwDmWYIvj1czGImPfXWdW
"""

#pip install apache-airflow

from datetime import date
import datetime
import pandas as pd

from airflow import DAG
from airflow.operators.bash import BashOperator

# Importar PythonOperator arriba del archivo
from airflow.operators.python import PythonOperator

import psycopg2
import csv
import boto3

s3 = boto3.resource(
    service_name="s3",
    aws_access_key_id = "AKIA4PFNY54U34VBUBRF",
    aws_secret_access_key = "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"
    )


def FiltrarDatos():
  hoy = date.today().strftime('%Y-%m-%d')
  url1= s3.Bucket('data-recomendaciones').Object('advertiser_ids.csv').get()
  url2= s3.Bucket('data-recomendaciones').Object('ads_views.csv').get()
  url3= s3.Bucket('data-recomendaciones').Object('product_views.csv').get()
    
  adv_ids = pd.read_csv(url1['Body'])
  ads_views = pd.read_csv(url2['Body'])
  product_views = pd.read_csv(url3['Body'])

  #Listado de views de advertisers activos
  ads_views_today = ads_views[ads_views['date'] == hoy]
  ads_views_activos = pd.merge(ads_views_today, adv_ids, on = 'advertiser_id', how = 'inner')
  ads_views_activos.to_csv("ads_views_activos.csv")
  s3.Bucket("data-recomendaciones").upload_file(Filename="ads_views_activos.csv",Key="ads_views_activos.csv")

  #Log de vistas de productos en la página del cliente
  product_views_today = product_views[product_views['date'] == hoy]
  product_views_activos = pd.merge(product_views_today, adv_ids, on = 'advertiser_id', how = 'inner')
  product_views_activos.to_csv("product_views_activos.csv")
  s3.Bucket("data-recomendaciones").upload_file(Filename="product_views_activos.csv",Key="product_views_activos.csv")

def TopProduct ():
  prod_views_activos = s3.Bucket('data-recomendaciones').Object('product_views_activos.csv').get()
  prod_views_activos_2 = pd.read_csv(prod_views_activos['Body'])
  prod_views_activos_2['count']=1
  TopProduct_final=prod_views_activos_2.groupby(["advertiser_id","date",'product_id'], as_index=False).sum()
  TopProduct_final=TopProduct_final.sort_values(by = ["advertiser_id",'count'], ascending = False)
  TopProduct_final=TopProduct_final.groupby(["advertiser_id"]).head(20)
  TopProduct_final['Model'] = 'TopProduct'
  TopProduct_final.to_csv("TopProduct_final.csv")
  s3.Bucket("data-recomendaciones").upload_file(Filename="TopProduct_final.csv",Key="TopProduct_final.csv")
  
def TopCTR ():
  ads_views_activos = s3.Bucket('data-recomendaciones').Object('ads_views_activos.csv').get()
  ads_views_activos_2 = pd.read_csv(ads_views_activos['Body'])
  ads_views_activos_2['flag'] = 1
  ads_views_activos_pivot = pd.pivot_table(ads_views_activos_2, index=['advertiser_id','product_id', 'date'], columns = ['type'], values = ['flag'], aggfunc = {'flag' : 'sum'}).reset_index()
  ads_views_activos_pivot['rate'] = ads_views_activos_pivot['flag']['click'].fillna(0)/ads_views_activos_pivot['flag']['impression']
  TopCTR_final = ads_views_activos_pivot.sort_values(by = 'rate', ascending = False)
  TopCTR_final.columns = [ 'advertiser_id', 'product_id', 'date', 'click','impression','rate']
  TopCTR_final = TopCTR_final.groupby(['advertiser_id']).head(20)
  TopCTR_final['Model'] = 'TopCTR'
  TopCTR_final.to_csv("TopCTR_final.csv")
  s3.Bucket("data-recomendaciones").upload_file(Filename="TopCTR_final.csv",Key="TopCTR_final.csv")
  

from operator import concat
engine = psycopg2.connect(
      database="postgres",
      user='postgres',
      password='riverplate1995',
      host="grupo-kvd.c7ezedheahhk.us-east-1.rds.amazonaws.com",
      port='5432'
  )

def DBWriting ():
  #### Tabla TOPProduct ####
  TopProduct = s3.Bucket('data-recomendaciones').Object('TopProduct_final.csv').get()
  TopProduct_final = pd.read_csv(TopProduct['Body'])
  cursor = engine.cursor()
  cursor.execute("""CREATE TABLE IF NOT EXISTS base_TopProduct_Final (advertiser_id VARCHAR, fecha_act DATE, product_id VARCHAR);""")
        
  for i in range(0 ,len(TopProduct_final)):
      values = (TopProduct_final['advertiser_id'][i], TopProduct_final['date'][i], TopProduct_final['product_id'][i]  )
      cursor.execute("INSERT INTO base_TopProduct_Final (advertiser_id, fecha_act, product_id) VALUES (%s, %s, %s)",
                  values)
  engine.commit()

  #### Tabla TOPCTR ####
  TopCTR = s3.Bucket('data-recomendaciones').Object('TopCTR_final.csv').get()
  TopCTR_final = pd.read_csv(TopCTR['Body'])
  cursor = engine.cursor()
  cursor.execute("""CREATE TABLE IF NOT EXISTS base_TopCTR_Final (advertiser_id VARCHAR,product_id VARCHAR, fecha_act DATE, click INT, impression INT, rate DECIMAL);""")
        
  for i in range(0 ,len(TopCTR_final)):
      values = (TopCTR_final['advertiser_id'][i],TopCTR_final['product_id'][i] , TopCTR_final['date'][i], TopCTR_final['click'][i], TopCTR_final['impression'][i], TopCTR_final['rate'][i])
      cursor.execute("INSERT INTO base_TopCTR_Final (advertiser_id,product_id, fecha_act, click, impression, rate) VALUES (%s, %s, %s, %s, %s, %s)",
                  values)
  engine.commit()


with DAG(
    dag_id='Pipeline_TP_final',
    schedule_interval='@Daily',
    start_date=datetime.datetime(2022, 4, 1),
    catchup=True,
) as dag:

    FiltrarDatos = PythonOperator(
    task_id='FiltrarDatos',
    python_callable=FiltrarDatos
    )

    TopProduct = PythonOperator(
    task_id='TopProduct',
    python_callable=TopProduct
    )
    
    TopCTR = PythonOperator(
    task_id='TopCTR',
    python_callable=TopCTR
    )

    DBWriting = PythonOperator(
    task_id='DBWriting',
    python_callable=DBWriting
    )

### dependencias

FiltrarDatos >> TopProduct
FiltrarDatos >> TopCTR
[TopCTR, TopProduct] >> DBWriting
