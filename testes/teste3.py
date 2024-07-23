# TESTE INTERNAÇÃO
import pandas as pd

# Lê o arquivo Excel em um DataFrame
df = pd.read_excel("atendimentos v3.xls")

colunas_guia = [7797731, 7545094, 'GUIA_ATENDIMENTO', 'GUIA_CONTA', 'GIH_NUMERO']

df_filtered_guia = df[df.isin(colunas_guia).any(axis=1)]

df_filtered_guia = df_filtered_guia[df_filtered_guia['CTH_NUM'] == 1 ]
df_filtered_guia = df_filtered_guia[df_filtered_guia['GUIA_CONTA'] == df_filtered_guia['GIH_NUMERO']]
# Mostra as colunas filtradas de interesse
df_filtered = df_filtered_guia[['HSP_NUM', 'HSP_PAC', 'CTH_NUM', 'FAT_SERIE', 'FAT_NUM', 'GUIA_ATENDIMENTO', 'GUIA_CONTA', 'GIH_NUMERO']]


print("Linhas onde a guia é encontrada:")
print(df_filtered)

