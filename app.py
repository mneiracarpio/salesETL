import cx_Oracle
import pandas as pd
import sqlalchemy 
from config import config

# SET conection configuration
acces_config = config['development']

# EXTRACT
############

#source_connection = cx_Oracle.connect('mneira/mneira@localhost:1521/XEPDB1')
source_connection = cx_Oracle.connect(
    user=acces_config.DB_SOURCE_USERNAME,
    password=acces_config.DB_SOURCE_PASSWORD,
    dsn=acces_config.DB_SOURCE_DSN,
    encoding=acces_config.DB_SOURCE_ENCODING
)

query = ('SELECT s.sale_id, s.client_id, p.product_id, p.product_name, c.first_name, c.last_name, p.category, s.sale_date, s.total_price '
 ' FROM sale s'
 ' JOIN client c ON (s.client_id = c.client_id)'
 ' JOIN product p ON (s.product_id = p.product_id)' )
df = pd.read_sql(query, source_connection)
source_connection.close()

# Show DataFrame
print("Original Data Frame")
print(df)

#TRANSFORMATION 1
#################

df['YEAR_SALE'] = df['SALE_DATE'].dt.year
df['MONTH_SALE'] = df['SALE_DATE'].dt.month
df['CLIENT_NAME'] = df['FIRST_NAME'].str.cat(df['LAST_NAME'], sep=' ')
df = df.drop(columns=['SALE_DATE'])
df = df.drop(columns=['FIRST_NAME'])
df = df.drop(columns=['LAST_NAME'])

#LOAD #1 - ORACLE - Sales Summary

# set new table
t1_table_name = 'sales_summary'
#engine = sqlalchemy.create_engine('oracle+cx_oracle://mneira:mneira@localhost:1521/?service_name=XEPDB1')
engine_t1 = sqlalchemy.create_engine(
    "oracle+cx_oracle://",
    connect_args={
        "user": acces_config.DB_T1_USERNAME,
        "password": acces_config.DB_T1_PASSWORD,
        "dsn": acces_config.DB_T1_DSN,
        "encoding": acces_config.DB_T1_ENCODING
    }
)

# set float fields
dtype = {'TOTAL_PRICE': sqlalchemy.Float}
df.to_sql(t1_table_name, con=engine_t1, if_exists='replace', index=False, dtype=dtype)
engine_t1.dispose()

# Show Data Frame
print("Sales Summary Data Frame")
print(df)



# LOAD #2 - MySQL - Product Summary
###################################

# TRANSFORMATION LOAD #2
df_product = df.groupby(['PRODUCT_ID', 'PRODUCT_NAME', 'CATEGORY']).agg({'TOTAL_PRICE': ['sum', 'count']}).reset_index()
df_product.columns = ['PRODUCT_ID', 'PRODUCT_NAME', 'CATEGORY', 'TOTAL_PRICE_SUM', 'PRODUCT_COUNT']

# Load #2
#mysql_engine = sqlalchemy.create_engine('mysql://report_app:report@localhost:3307/reports')
engine_t2 = sqlalchemy.create_engine(
    "mysql+mysqlconnector://",
    connect_args={
        "user": acces_config.DB_T2_USERNAME,
        "password": acces_config.DB_T2_PASSWORD,
        "host": acces_config.DB_T2_HOST,
        "port": acces_config.DB_T2_PORT,
        "database": acces_config.DB_T2_DB
    }
)
t2_table_name = 'product_summary'
df_product.to_sql(t2_table_name, con=engine_t2, if_exists='replace', index=False, dtype=dtype)
engine_t2.dispose()

# Show Data Frame
print("Product Summary Data Frame")
print(df_product)


# LOAD #3 - MySQL - Category Summary
####################################

# TRANSFORMATION LOAD #3
df_categpry = df.groupby(['YEAR_SALE','CATEGORY']).agg({'TOTAL_PRICE': ['sum', 'count']}).reset_index()
df_categpry.columns = ['YEAR_SALE', 'CATEGORY', 'TOTAL_PRICE_SUM', 'SALES_COUNT']

# Load #3
engine_t3 = sqlalchemy.create_engine(
    "mysql+mysqlconnector://",
    connect_args={
        "user": acces_config.DB_T3_USERNAME,
        "password": acces_config.DB_T3_PASSWORD,
        "host": acces_config.DB_T3_HOST,
        "port": acces_config.DB_T3_PORT,
        "database": acces_config.DB_T3_DB
    }
)
t3_table_name = 'category_summary'
df_categpry.to_sql(t3_table_name, con=engine_t3, if_exists='replace', index=False, dtype=dtype)
engine_t3.dispose()

# Show Data Frame
print("Category Summary Data Frame")
print(df_categpry)

