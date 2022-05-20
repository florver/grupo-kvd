# -*- coding: utf-8 -*-
"""con_rds.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1s_2Txpr7oFLXN9WklLdvA_Fcz_SXJWcB
"""

import io
import pandas as pd 
import datetime
from datetime import date
import json

import psycopg2

engine = psycopg2.connect(
    database="postgres",
    user='postgres',
    password='riverplate1995',
    host="grupo-kvd.c7ezedheahhk.us-east-1.rds.amazonaws.com",
    port='5432'
)

#### Tabla TOPCTR ####
cursor = engine.cursor()
cursor.execute("""SELECT * FROM base_TopCTR_Final""")
data_TopCTR = cursor.fetchall()

cols=[]
for elt in cursor.description:
  cols.append(elt[0])
df_ctr = pd.DataFrame(data=data_TopCTR, columns=cols)
print(df_ctr.head())

#### Tabla TOPProduct ####
cursor = engine.cursor()
cursor.execute("""SELECT * FROM base_TopProduct_Final""")
data_TopProduct = cursor.fetchall()

cols=[]
for elt in cursor.description:
  cols.append(elt[0])
df_tp = pd.DataFrame(data=data_TopProduct, columns=cols)


print(df_tp.head())