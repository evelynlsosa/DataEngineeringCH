import requests
import json
import pandas as pd
import psycopg2
from datetime import datetime, timedelta

# Configuración de la API
api_url = "https://apitransporte.buenosaires.gob.ar/datos/movilidad/transito"
client_id = "1a4ba29ff7c34e219c119313009d9193"
client_secret = "014FffaEb3A343b5A7243fF3D4625BE0"

# Configuración de Amazon Redshift
redshift_credentials = {
    "dbname": "tu_database",
    "user": "",
    "password": "",
    "host": "tu_host_redshift",
    "port": "5439"
}

# Obtener fecha actual y fecha hace tres meses
fecha_actual = datetime.now()
fecha_tres_meses_atras = fecha_actual - timedelta(days=90)

# Formatear fechas en el formato esperado por la API
fecha_actual_str = fecha_actual.strftime("%Y-%m-%dT%H:%M:%S")
fecha_tres_meses_atras_str = fecha_tres_meses_atras.strftime("%Y-%m-%dT%H:%M:%S")

# Parámetros de la API
params = {
    "client_id": client_id,
    "client_secret": client_secret,
    "fecha_desde": fecha_tres_meses_atras_str,
    "fecha_hasta": fecha_actual_str
}

# Realizar solicitud a la API
response = requests.get(api_url, params=params)

# Verificar si la solicitud fue exitosa (código de estado 200)
if response.status_code == 200:
    # Convertir la respuesta JSON a un diccionario de Python
    data_dict = response.json()

    # Crear un DataFrame de Pandas desde el diccionario
    df = pd.DataFrame(data_dict)

    # Conectar a Amazon Redshift
    conn = psycopg2.connect(
        dbname=redshift_credentials["dbname"],
        user=redshift_credentials["user"],
        password=redshift_credentials["password"],
        host=redshift_credentials["host"],
        port=redshift_credentials["port"]
    )

    # Crear una tabla en Redshift y cargar datos
    with conn.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS datos_movilidad (
                ConteoTransito INT,
                hora TIMESTAMP,
                location_code VARCHAR(255),
                sentido VARCHAR(255),
                cantidad INT
            )
        """)

        conn.commit()

        # Cargar datos en la tabla
        df.to_sql("datos_movilidad", conn, index=False, if_exists="append", dtype={
            'hora': 'TIMESTAMP'
        })

    # Cerrar la conexión a Redshift
    conn.close()

    print("Datos cargados exitosamente en Redshift.")
else:
    print(f"Error al obtener datos de la API. Código de estado: {response.status_code}")
