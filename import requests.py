import requests
import psycopg2

# Configuración de la API
api_url = 'https://apis.datos.gob.ar/series/api/series/?ids=168.1_T_CAMBIOR_D_0_0_26&start_date=2018-07&limit=5000'

# Configuración de Redshift
redshift_config = {
    'dbname': ',
    'user': '',
    'password': ',
    'host': '',
    'port': '',
}

# Obtener datos de la API
response = requests.get(api_url)
data = response.json()

# Conectar a Redshift
conn = psycopg2.connect(**redshift_config)
cursor = conn.cursor()

# Crear tabla en Redshift 
create_table_query = """
    CREATE TABLE IF NOT EXISTS tipo_de_cambio (
        fecha DATE,
        valor NUMERIC,
        
    );
"""

cursor.execute(create_table_query)
conn.commit()

# Insertar datos en la tabla
insert_query = """
    INSERT INTO tipo_de_cambio (fecha, valor)
    VALUES (%s, %s);
"""

for registro in data['data']['168.1_T_CAMBIOR_D_0_0_26']['values']:
    values = (registro['period'], registro['value'])
    cursor.execute(insert_query, values)

conn.commit()

# Cerrar conexiones
cursor.close()
conn.close()
