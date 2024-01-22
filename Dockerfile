# Usa la imagen oficial de Apache Airflow
FROM apache/airflow:2.8.0

# Instala las dependencias necesarias
USER root
RUN pip install requests pandas psycopg2-binary

# Copia tu script y DAG al directorio de trabajo del contenedor
COPY ./tu_script.py /usr/local/airflow/dags/tu_script.py
COPY ./tu_dag.py /usr/local/airflow/dags/tu_dag.py

# Cambia el propietario del directorio y archivos para el usuario de Airflow
RUN chown -R airflow: /usr/local/airflow/dags

# Cambia al usuario de Airflow
USER airflow
