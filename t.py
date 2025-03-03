# select * from flight db

import sqlite3  
import pandas as pd
conn = sqlite3.connect('flights-test.db')
cursor = conn.cursor()
df = pd.read_sql_query("SELECT * FROM flights", conn)    
print(df)