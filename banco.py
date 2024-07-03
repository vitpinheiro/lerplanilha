import pyodbc

SERVER = r"10.1.3.196,50000"
DATABASE = "SMARTTESTE"
USERNAME = "smrtusr"
PASSWORD = "SMART2023#"

connectionString = f'DRIVER={{SQL Server}};SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD}'

conn = pyodbc.connect(connectionString)
