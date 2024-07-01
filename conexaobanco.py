import pymysql
def connect_to_database():
    try:
        connection = pymysql.connect(
            host='localhost',      # Substitua pelo endereço do seu servidor de banco de dados
            user='root',  # Substitua pelo seu nome de usuário
            password='',  # Substitua pela sua senha
            database='teste'   # Substitua pelo nome do seu banco de dados
        )
        return connection
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None
    
    # Função para executar uma consulta SQL no banco de dados conectado
def execute_sql_query(query):
    connection = connect_to_database()
    if connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchone()  # Retorna apenas a primeira linha da consulta

                if result:
                    return result[0]  # Retorna o primeiro valor da primeira coluna
                else:
                    return None

        except Exception as e:
            print(f"Erro ao executar consulta SQL: {e}")
            return None
        finally:
            connection.close()
    else:
        return None