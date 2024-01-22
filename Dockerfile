# Usar la imagen oficial de Apache Airflow
FROM apache/airflow:2.8.0

# Instalar las dependencias necesarias
USER root
RUN pip install requests pandas psycopg2-binary

# Copiar el script y DAG al directorio de trabajo del contenedor
COPY ./ApiMovilidadTransito.py /usr/local/airflow/dags/ApiMovilidadTransito.py
COPY ./Dag.py /usr/local/airflow/dags/Dag.py

# Cambiar el propietario del directorio y archivos para el usuario de Airflow
RUN chown -R airflow: /usr/local/airflow/dags

# Cambiar al usuario de Airflow
USER airflow
