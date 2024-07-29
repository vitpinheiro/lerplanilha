import pyodbc

# Configurações da conexão
server = r'10.1.3.196,50000'  # Substitua pelo nome do seu servidor SQL Server
database = 'SMARTTESTE'  # Substitua pelo nome do seu banco de dados
username = 'smrtusr'  # Substitua pelo seu nome de usuário
password = 'SMART2023#'  # Substitua pela sua senha


# String de conexão
connection_string = f'DRIVER=ODBC Driver 17 for SQL Server;SERVER={server};DATABASE={database};UID={username};PWD={password};'

try:
    # Conectando ao banco de dados
    connection = pyodbc.connect(connection_string)

 
    cursor = connection.cursor()
    query = query
    cursor.execute(query)


    row = cursor.fetchone()
    while row:
        print(row)
        row = cursor.fetchone()

except Exception as e:
    print(f"Erro ao conectar ao banco de dados: {e}")

finally:
    # Fechando a conexão
    if 'connection' in locals():
        connection.close()
