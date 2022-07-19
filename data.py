
import logging
import requests
import pandas as pd
from datetime import datetime
from urls import cinema_url, library_url, museum_url


current_datetime1 = datetime.now().strftime("%Y-%m")
current_datetime1 = str(current_datetime1)
current_datetime2 = datetime.now().strftime("%d-%m-%Y")
current_datetime2 = str(current_datetime2)


"""
Logging is a means of tracking events that happen when some software runs. 
The software developer adds logging calls to their code to indicate that certain 
events have occurred.

documentation: https://docs.python.org/3/library/logging.html
"""
logging.basicConfig(level=logging.INFO, format='%(asctime)s: %(levelname)s - %(message)s')


#Making csv files
"""
Requests allows you to send HTTP/1.1 requests extremely easily. There is no need to manually 
add query strings to your URLs, or to form-encode your POST data. Keep-alive and HTTP connection 
pooling are 100% automatic, thanks to urllib3.

documentation: https://requests.readthedocs.io/en/master/user/quickstart/
"""
try:
    
    logging.info("Making csv files")
    museum = requests.get(museum_url, allow_redirects=True)
    cinema = requests.get(cinema_url, allow_redirects=True)
    library = requests.get(library_url, allow_redirects=True)
    open("museos"+"\\"+current_datetime1+"\\"+"museos-"+current_datetime2+".csv", "wb").write(museum.content)
    open("cines"+"\\"+current_datetime1+"\\"+"cines-"+current_datetime2+".csv", "wb").write(cinema.content)
    open("bibliotecas"+"\\"+current_datetime1+"\\"+"bibliotecas-"+current_datetime2+".csv", "wb").write(library.content)
except Exception as e:
    logging.error(e)

#Normalizing data
try:
    logging.info('Normalizing data')
    df_museum = pd.read_csv("museos"+"\\"+current_datetime1+"\\"+"museos-"+current_datetime2+".csv", sep=',', encoding='UTF-8')
    df_museum.rename(columns = {"categoria":"Categoría", "provincia":"Provincia","localidad":"Localidad",
                            "nombre":"Nombre", "direccion":"Domicilio", "telefono":"Teléfono",
                            "fuente":"Fuente"}, inplace = True)

    df_cinema = pd.read_csv("cines"+"\\"+current_datetime1+"\\"+"cines-"+current_datetime2+".csv", sep=',', encoding='UTF-8')

    df_library = pd.read_csv("bibliotecas"+"\\"+current_datetime1+"\\"+"bibliotecas-"+current_datetime2+".csv", sep=',', encoding='UTF-8')
    df_library.rename(columns = {'Domicilio':'Dirección'}, inplace = True)

    main_df = pd.concat([df_museum, df_cinema, df_library])
except Exception as e:
    logging.error(e) 


#Making tables
try:
    logging.info("Making tables")
    # table 1
    main_table = main_df.loc[:,["Cod_Loc","IdProvincia","IdDepartamento","Categoría","Provincia","Localidad",
                       "Nombre","Domicilio","CP","Teléfono","Mail","Web"]]
    main_table["Fecha de carga"] = pd.to_datetime('today').strftime("%d-%m-%Y")

    # table 2
    categories_table_1 = main_df.groupby(["Categoría"]).size().to_frame(name = "Total por categoría")
    categories_table_2 = main_df.groupby(["Categoría","Fuente"]).size().to_frame(name = "Total por fuente")
    categories_table_3 = main_df.groupby(["Categoría","Provincia"]).size().to_frame(name = "Categorías por provincia")
    categories_table = categories_table_1.merge(categories_table_2, how="outer", left_index=True, right_index=True)
    categories_table = categories_table.merge(categories_table_3, how="outer", left_index=True, right_index=True)
    categories_table.reset_index(inplace=True)
    categories_table.set_index("Categoría", inplace=True)
    categories_table = categories_table[["Total por categoría","Fuente","Total por fuente","Provincia","Categorías por provincia"]]
    categories_table["Fecha de carga"] = pd.to_datetime("today").strftime("%d-%m-%Y")

    # talbe 3
    cinema_table = df_cinema.loc[:,["Provincia","Pantallas","Butacas","espacio_INCAA"]]
    aggregation_functions = {"Pantallas": "sum", "Butacas": "sum","espacio_INCAA": "count"}
    cinema_table = cinema_table.groupby(cinema_table["Provincia"]).aggregate(aggregation_functions)
    cinema_table['Fecha de carga'] = pd.to_datetime("today").strftime("%d-%m-%Y")

except Exception as e:
    logging.error(e)

