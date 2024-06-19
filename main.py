import pandas as pd
import streamlit as st

# Função para ler e filtrar o arquivo XLS
def read_and_filter_xls(xls_file, column_names):
    try:
        # Ler o arquivo XLS e criar DataFrame
        df = pd.read_excel(xls_file)

        # Filtrar apenas as colunas especificadas
        df_filtered = df[column_names]

        return df_filtered
    
    except FileNotFoundError:
        st.error(f"Arquivo não encontrado: {xls_file}")
    except Exception as e:
        st.error(f"Ocorreu um erro: {e}")
        return None

# Caminho para o arquivo XLS
xls_file = "Demonstrativo original 04-2024.xls"

# Lista de colunas para exibir
column_names = ['Guia', 'Dt item']

# Interface do Streamlit
st.title('Leitura e Filtro de Arquivo XLS')

# Text input para nome da coluna
col_name = st.text_input('Digite o nome da coluna', 'Guia')

# Ler e filtrar o arquivo XLS
df_filtered = read_and_filter_xls(xls_file, column_names)

# Exibir o DataFrame filtrado se existir
if df_filtered is not None:
    st.write(f'Tabela filtrada pela coluna "{col_name}":')
    
    # Verificar se o nome da coluna digitado está presente no DataFrame
    if col_name in df_filtered.columns:
        st.table(df_filtered[[col_name]])
    else:
        st.warning(f'Coluna "{col_name}" não encontrada no DataFrame.')
