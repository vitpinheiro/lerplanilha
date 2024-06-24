import pandas as pd

# Lê o arquivo Excel em um DataFrame
df = pd.read_excel("ATENDIMENTOS.xls")

colunas_guia = ['9148728', 'GUIA_ATENDIMENTO', 'GUIA_CONTA', 'GIH_NUMERO']

df_filtered_guia = df[df.isin(colunas_guia).any(axis=1)]

df_filtered_guia = df_filtered_guia[df_filtered_guia['CTH_NUM'] == 1]
# Mostra as colunas filtradas de interesse
df_filtered = df_filtered_guia[['HSP_NUM', 'HSP_PAC', 'CTH_NUM', 'FAT_SERIE', 'FAT_NUM']]


print("Linhas onde a guia é encontrada:")
print(df_filtered)

# Verifica se alguma linha foi filtrada
if not df_filtered.empty:
    print("Linhas onde é igual a '9148728', 'GUIA_ATENDIMENTO', 'GUIA_CONTA' ou 'GIH_NUMERO':")
    print(df_filtered_guia)
else:
    print("A guia não foi encontrada no DataFrame.")
