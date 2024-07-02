
import pymysql

def connect_to_database():
    try:
        connection = pymysql.connect(
            host='10.1.3.196',      # Substitua pelo endereço do seu servidor de banco de dados
            user='smrtusr',  # Substitua pelo seu nome de usuário
            password='SMART2023#',  # Substitua pela sua senha
            database='SMARTTESTE'   # Substitua pelo nome do seu banco de dados
        )
        return connection
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None


connection = connect_to_database()
if connection:
    print("Conexão bem-sucedida!")
    connection.close()  
else:
    print("Falha ao conectar ao banco de dados.")
