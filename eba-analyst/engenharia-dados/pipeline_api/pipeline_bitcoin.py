import requests
import psycopg2
import os
from dotenv import load_dotenv

##from tinydb import TinyDB
from datetime import datetime
import time

# Carregar as configurações do arquivo .env
load_dotenv()


# Função para extrair dados do bitcoin
def extract_bitcoin_data():
    url = "https://api.coinbase.com/v2/prices/spot"

    response = requests.get(url)
    data = response.json()
    return data


# função para transformar os dados
def transform_bitcoin_data(data):
    valor = data["data"]["amount"]
    cripto = data["data"]["base"]
    moeda = data["data"]["currency"]
    timestamp = datetime.now()

    transformed_data = {
        "valor": valor,
        "cripto": cripto,
        "moeda": moeda,
        "timestamp": timestamp,
    }
    return transformed_data


# Criar tabela no Banco de dados (executado apenas uma vez)
def create_table():
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
        )
        with conn.cursor() as cur:
            cur.execute(
                """
                        CREATE TABLE IF NOT EXISTS bitcoin_table (
                        id SERIAL PRIMARY KEY,
                        valor NUMERIC NOT NULL,
                        cripto VARCHAR(10) NOT NULL,
                        moeda VARCHAR (10) NOT NULL,
                        timestamp TIMESTAMP NOT NULL)"""
            )
            conn.commit()
            print("Tabela criada/verificada com SUCESSO!!")
    except Exception as e:
        print(f"Erro ao criar tabela: {e}")
    finally:
        if conn:
            conn.close()


# função para carregar os dados no PostgreSQL
def load_bitcoin_postgres(data):
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
        )
        with conn.cursor() as curr:
            curr.execute(
                """
                INSERT INTO bitcoin_table (valor, cripto, moeda, timestamp)
                VALUES (%s, %s, %s, %s)
                        """,
                (data["valor"], data["cripto"], data["moeda"], data["timestamp"]),
            )
            conn.commit()
            print("Carregamento Realizado com SUCESSO!!")
    except Exception as e:
        print(f"Erro ao carregar os dados {e}")
    finally:
        if conn:
            conn.close()


##Essa função era para trabalhar com um banco de dados NOcicle
# def load_bitcoin_tinydb(data, db_name="bitcoin_json"):
# db = TinyDB(db_name)
# db.insert(data)
# print("Carregamento Realizado com Suceso!!")


if __name__ == "__main__":
    # Criação da tabela para inicialização
    create_table()

    # Loop principal
    try:
        while True:
            data = extract_bitcoin_data()
            transformed_data = transform_bitcoin_data(data)
            load_bitcoin_postgres(transformed_data)
            time.sleep(12)
    except KeyboardInterrupt:
        print("Execução foi INTERROMPIDA pelo Usuário!!")
