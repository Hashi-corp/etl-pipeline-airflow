from airflow import DAG
from airflow.providers.http.hooks.http import HttpHook
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.decorators import task
from airflow.utils.dates import days_ago
import logging

LATITUDE = 13.1781
LONGITUDE = 80.2886
POSTGRESS_CONN_ID = 'postgres_default'
API_CONN_ID = 'open_meteo_api'
API_ENDPOINT = 'v1/forecast?latitude={}&longitude={}&current_weather=true'

default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
}

with DAG(
    dag_id='etl_weather_data',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False
    ) as dags:
    
    @task
    def fetch_weather_data():
        """Fetch weather data from the API using Airflow connection."""
        http_hook = HttpHook(method='GET', http_conn_id=API_CONN_ID)
        url = API_ENDPOINT.format(LATITUDE, LONGITUDE)
        
        response = http_hook.run(endpoint=url)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to fetch data: {response.text}")
        
    @task
    def transform_weather_data(weather_data):
        """Transform the weather data to extract relevant fields."""
        try:
            current_weather = weather_data['current_weather']
            transformed_data = {
                                'latitude': LATITUDE,
                                'longitude': LONGITUDE,
                                'time': current_weather.get('time', None), 
                                'temperature': current_weather.get('temperature', None),
                                'windspeed': current_weather.get('windspeed', None),
                                'weathercode': current_weather.get('weathercode', None)
                                }
            logging.info(f"Transformed data: {transformed_data}")
            return transformed_data
        
        except Exception as e:
            logging.error(f"Error transforming data: {e}")
            raise 
    
    @task
    def load_weather_data(transformed_data):
        """Load the transformed data into PostgreSQL."""
        if not transformed_data:
            raise ValueError("No data to load into PostgreSQL.")
        
        # Create a connection to PostgreSQL
        pg_hook = PostgresHook(postgres_conn_id=POSTGRESS_CONN_ID)
        conn = pg_hook.get_conn()
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS weather_data (
                latitude FLOAT,
                longitude FLOAT,
                time TIMESTAMP,
                temperature FLOAT,
                windspeed FLOAT,
                weathercode INT
            )
        """)

        #insert data
        cursor.execute("""
            INSERT INTO weather_data (latitude, longitude, time, temperature, windspeed, weathercode)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            transformed_data['latitude'],
            transformed_data['longitude'],
            transformed_data['time'],
            transformed_data['temperature'],
            transformed_data['windspeed'],
            transformed_data['weathercode']
        ))

        conn.commit()
        conn.close()

#DAG Workflow: ETL Pipeline
weather_data = fetch_weather_data()
transformed_data = transform_weather_data(weather_data)
load_weather_data(transformed_data)