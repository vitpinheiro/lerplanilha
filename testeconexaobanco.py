import pymysql
import pandas as pd
import streamlit as st
# Função para conectar ao banco de dados MySQL
def connect_to_database():
    try:
        connection = pymysql.connect(
            host='localhost',      # Substitua pelo endereço do seu servidor de banco de dados
            user='root',  # Substitua pelo seu nome de usuário
            password='',  # Substitua pela sua senha
            database='centrocirurgico'   # Substitua pelo nome do seu banco de dados
        )
        return connection
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

# Função para executar uma consulta SQL e retornar os resultados como um DataFrame
def execute_query(query):
    connection = connect_to_database()
    if connection:
        try:
            df = pd.read_sql(query, connection)
            return df
        except Exception as e:
            print(f"Erro ao executar a consulta: {e}")
            return None
        finally:
            connection.close()
    else:
        return None

# Exemplo de uso
query = "SELECT nome FROM cirurgioes"
df = execute_query(query)
if df is not None:
    print(df)
else:
    print("Falha ao obter dados do banco de dados.")
st.table(df)