import requests
import datetime
import requests
import config
import json
from hdfs import InsecureClient
import pyspark.sql.functions as F
import pandas as pd
from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
from sqlalchemy import create_engine

url = "https://admindata.atmo-france.org/api/login"
data = {
    "username": config.username,
    "password": config.mdp
}

token = requests.post(url, json=data)

# Obtenir la date du jour
aujourdhui = datetime.date.today()
aujourdhui_formatte = aujourdhui.strftime('%Y-%m-%d')

# URL de l'API avec la date d'aujourd'hui
api_link = f'https://admindata.atmo-france.org/api/data/112/%7B%22date_ech%22%3A%7B%22operator%22%3A%22%3D%22%2C%22value%22%3A%22{aujourdhui_formatte}%22%7D%7D'

# # Token d'authentification
token = token.json().get('token')
# Paramètres d'en-tête pour inclure le token dans la requête
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# Envoyer la requête GET à l'API avec les paramètres d'en-tête
response = requests.get(api_link, headers=headers)

# Vérifier que la requête a réussi (code de statut 200)
if response.status_code == 200:
        # Récupérer les données de réponse
        data = response.json()

        # Créer un client Hadoop
        client = InsecureClient('http://127.0.0.1:9870')

        # Envoyer les données au format JSON au cluster Hadoop
        with client.write(f'/indice_qualite/{aujourdhui_formatte}.json', encoding='utf-8') as writer:
            json.dump(data, writer)
else:
    print(f"La requête a échoué avec le code d'erreur {response.status_code}")


# Connection spark hadoop
spark = SparkSession.builder.appName("HDFSRead").getOrCreate()
hdfs_home_path = "hdfs://localhost:9000/"


# Read a file from Hadoop into a DataFrame
indice_qualite = spark.read.json(hdfs_home_path + f'/indice_qualite/{aujourdhui_formatte}.json')

# Décomposer la liste en plusieurs lignes
indice_qualite = indice_qualite.select(F.explode("features.properties").alias("properties"))

# # Extraire les données d'intérêt
indice_qualite = indice_qualite.select(F.col("properties.gml_id").alias('iq_id'), 
            F.col('properties.date_maj').alias('date_maj'),
            F.col("properties.code_no2").alias("code_no2"),
            F.col("properties.code_o3").alias("code_o3"),
            F.col("properties.code_pm10").alias("code_pm10"),
            F.col("properties.code_pm25").alias("code_pm25"),
            F.col("properties.code_qual").alias("code_qual"),
            F.col("properties.code_so2").alias("code_so2"),
            F.col("properties.lib_qual").alias("qual_name"),
            F.col("properties.code_zone").alias("zone_code"),
            F.col("properties.lib_zone").alias("zone_name"),
            F.col("properties.type_zone").alias("type_zone"),
            F.col("properties.date_dif").alias("date_dif"),
            F.col("properties.date_ech").alias("date_alerte"),
            F.col("properties.aasqa").alias("source_code"),
            F.col("properties.source").alias("source_name"),
            F.col("properties.x_wgs84").alias("x_wgs84"),
            F.col("properties.y_wgs84").alias("y_wgs84") )

indice_qualite_pd = indice_qualite.toPandas()

my_conn = create_engine(f"mysql+pymysql://{config.user_opolo}:{config.password}@mysql-ipssi2.alwaysdata.net/ipssi2_hadoo").connect()
my_conn.rollback() # Rollback any pending transactions
indice_qualite_pd.to_sql(con=my_conn,name='indice_qualite',if_exists='append')