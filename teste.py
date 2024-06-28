# TESTE NOVO
# TRATAMENTO

import pandas as pd

# Lê o arquivo Excel em um DataFrame
df = pd.read_excel("atendimentos v3.xls")


colunas_guia = [8698702, 6063290, 'GUIA_ATENDIMENTO', 'GIH_NUMERO', 'FAT_NUM']

df_filtered_guia = df[df.isin(colunas_guia).any(axis=1)]

df_filtered_guia = df_filtered_guia[df_filtered_guia['CTH_NUM'] == 0]
df_filtered_guia = df_filtered_guia[pd.notna(df_filtered_guia['FAT_NUM'] )]
df_filtered_guia = df_filtered_guia[df_filtered_guia['GUIA_ATENDIMENTO'] == df_filtered_guia['GIH_NUMERO']]
# Mostra as colunas filtradas de interesse
df_filtered = df_filtered_guia[['CTH_NUM', 'GUIA_ATENDIMENTO','GIH_NUMERO', 'FAT_NUM']]


print("Linhas onde a guia é encontrada:")
print(df_filtered)


