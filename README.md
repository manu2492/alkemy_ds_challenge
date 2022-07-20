# Alkemy Data Analysis con Python Challenge 

## Ejecución

1. Clonar el repositorio:
```
git clone https://github.com/manu2492/alkemy_ds_challenge.git
```
2. Crear un entorno virtual dentro de la carpeta del proyecto:
```
python3 -m venv venv

```
3. Instalar las dependencias:
```
pip install -r requirements.txt

```
4. Configurar la conexión a la base de datos PostgreSQL. Crea un archivo `.env` en la raíz del proyecto. Dentro deberás crear las siguientes 3 variables, los nombres deben respetarse ya que se usan en el archivo `config.py` para crear la conexión a la base de datos.
```
USUARIO= your_user
PASS= your_password
DB_NAME= your_db_name
```
5. Ya puedes ejecutar el programa `create_tables.py` que realizará la descarga, procesamiento y actualización de la base de datos.
