# Usar la imagen oficial de Apache Airflow
FROM apache/airflow:2.8.0

# Instalar las dependencias necesarias
USER root
RUN pip install requests pandas psycopg2-binary

# Copiar el script y DAG al directorio de trabajo del contenedor
COPY ./tu_script.py /usr/local/airflow/dags/tu_script.py
COPY ./tu_dag.py /usr/local/airflow/dags/tu_dag.py

# Cambiar el propietario del directorio y archivos para el usuario de Airflow
RUN chown -R airflow: /usr/local/airflow/dags

# Cambiar al usuario de Airflow
USER airflow
