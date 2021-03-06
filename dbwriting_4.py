# -*- coding: utf-8 -*-
"""DBWriting_4.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1S8orS7TwwLyFrg1eO-H1bIhRYRttwYu6
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

#### Tabla TOPCTR ####
cursor = engine.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS base_TopCTR_Final (advertiser_id VARCHAR,product_id VARCHAR, fecha_act DATE, click DECIMAL, impression DECIMAL, rate DECIMAL);""")

#url= 'https://github.com/florver/grupo-kvd/blob/8626cb3f62d5ec77610b25a394b6a4f2340f1909/TopCTR_final.csv'

url='/home/ubuntu/grupo-kvd/TopCTR_final.csv'
df = pd.read_csv(url)

for i in range(0 ,len(df)):
    values = (df['advertiser_id'][i],df['product_id'][i] , df['date'][i], df['click'][i], df['impression'][i], df['rate'][i])
    cursor.execute("INSERT INTO base_TopCTR_Final (advertiser_id,product_id, fecha_act, click, impression, rate) VALUES (%s, %s, %s, %s, %s, %s)",
                values)

engine.commit()

#print("Records created successfully")
#conn.close()

##reader = df
##next(reader) 
##for row in reader:
##  cursor.execute(
##  "INSERT INTO base_TopCTR_Final VALUES (%s, %s, %s, %s, %s, %s)",
##  row
##  )
##engine.commit()

#with open('/TopCTR_final.csv', 'r') as f:
#    reader = csv.reader(f)
#    next(reader) 
#    for row in reader:
#        cursor.execute(
#        "INSERT INTO base_TopCTR VALUES (%s, %s, %s, %s, %s)",
#        row
#    )
#engine.commit()

cursor.execute("""select * from base_TopCTR_Final LIMIT 5""")
rows=cursor.fetchall()
for row in rows:
  print(row)
print("Termino query")
