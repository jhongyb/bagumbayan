import sqlite3
import pandas as pd
from datetime import datetime

def datevalue(d):
    if d:
        try:
            return datetime.strptime(d,'%m/%d/%Y').strftime('%Y-%m-%d')
        except:
            return datetime.strptime(d,'%m/%d/%Y').strftime('%Y-%m-%d')
    else:
        return ''

db=sqlite3.connect('db/db.sqlite3')
df=pd.read_csv('test.csv',encoding='latin')
data=df.values.tolist()
cur=db.cursor()
for i in data:
    try:
        cur.execute("INSERT INTO EMPLOYEE_BIOMETRIC (BIO_DATE,BIO_TIME,BIO_PUNCHSTATE,BIO_ID_ID) VALUES(?,?,?,?)",(datevalue(i[1]),i[2],i[3],i[0]))
        print(i[0])
    except Exception as e:
        print(f'{e} {i[0]}')
        db.rollback()
db.commit()
print('Success')