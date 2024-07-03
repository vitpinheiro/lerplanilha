import pandas as pd
import datetime as dt

df_1 = pd.read_excel("Demonstrativo original 04-2024.xls")

for data in df_1["Dt item"]:
    data_formatada = dt.datetime.strptime(data, '%d/%m/%Y')
    pass

df_2 = pd.read_excel("atendimentos v3.xls")

for data in df_2["CTH_DTHR_INI", ]:
    data = data.split(" ")
    data_sem_hora = data[0]
    data_formatada = dt.datetime.strptime(data_sem_hora, '%Y-%m-%d')
    pass
