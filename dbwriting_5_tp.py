# -*- coding: utf-8 -*-
"""DBWriting_5_TP.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1imhsxY9LnhDMX78AYTM92atiQcQqvlps
"""

#pip install psycopg2-binary

import psycopg2
import csv
import pandas as pd

engine = psycopg2.connect(
    database="postgres",
    user='postgres',
    password='riverplate1995',
    host="grupo-kvd.c7ezedheahhk.us-east-1.rds.amazonaws.com",
    port='5432'
)

#### Tabla Product ####
cursor = engine.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS base_TopProduct_Final (advertiser_id VARCHAR, fecha_act DATE, product_id VARCHAR, count INT);""")

url='/home/ubuntu/grupo-kvd/TopProduct_final.csv'
df = pd.read_csv(url)

for i in range(0 ,len(df)):
    values = (df['advertiser_id'][i] , df['date'][i],df['product_id'][i], df['count'][i])
    cursor.execute("INSERT INTO base_TopProduct_Final (advertiser_id, fecha_act, product_id, count) VALUES (%s, %s, %s, %s)",
                  values)

engine.commit()
#print("Records created successfully")
#conn.close()

cursor.execute("""select * from base_TopProduct_Final LIMIT 5""")
rows=cursor.fetchall()
for row in rows:
  print(row)
print("Termino query")
