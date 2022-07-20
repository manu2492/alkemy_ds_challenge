import logging
from data import main_table, categories_table, cinema_table
from datetime import datetime
from sqlalchemy import MetaData, Integer, Text
from config import USER, PASSWORD, DB_NAME

logging.basicConfig(level=logging.INFO, format='%(asctime)s: %(levelname)s - %(message)s')


#Database connection
logging.info('Connecting to postgresql')
engine = "postgresql://"+USER+":"+PASSWORD+"@localhost:5432/"+DB_NAME


#Uploading data to database
"""
to_sql() method allows you to write a DataFrame to a SQL table.
documentation: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_sql.html
"""
try:
    logging.info('Uploading main_table')
    main_table.to_sql(
        'main_table',
        engine,
        if_exists='replace',
        index=False,
        chunksize=500,
        dtype={
            "Cod_Localidad": Integer,
            "IdProvincia": Integer,
            "IdDepartamento": Integer,
            "Categoría":  Text,
            "Provincia": Text,
            "Localidad": Text,
            "Nombre": Text,
            "Dirección": Text,
            "CP": Text,
            "Teléfono": Text,
            "Mail": Text,
            "Web": Text
        })

    logging.info('Uploading categories_table')
    categories_table.to_sql(
        'categories_table',
        engine,
        if_exists='replace',
        chunksize=500,
        dtype={
            "Total por categoría": Integer,
            "Fuente": Text,
            "Total por fuente": Integer,
            "Provincia":  Text,
            "Categorías por provincia": Integer,
        })

    logging.info('Uploading cinema_table')
    cinema_table.to_sql(
        'cinema_table',
        engine,
        if_exists='replace',
        chunksize=500,
        dtype={
            "Provincia": Text,
            "Pantallas": Integer,
            "Butacas": Integer,
            "espacio_INCAA":  Text,
        })

except Exception as e:
    logging.error(e)
    logging.error('Error uploading tables')
    
