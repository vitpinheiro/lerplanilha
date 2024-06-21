import pandas as pd
import streamlit as st


# HORIZONTAL_RED = "images/horizontal_red.png"
# ICON_RED = "images/icon_red.png"
# HORIZONTAL_BLUE = "images/horizontal_blue.png"
# ICON_BLUE = "images/icon_blue.png"

# options = [HORIZONTAL_RED, ICON_RED, HORIZONTAL_BLUE, ICON_BLUE]
# sidebar_logo = st.selectbox("Sidebar logo", options, 0)
# main_body_logo = st.selectbox("Main body logo", options, 1)

# st.logo(sidebar_logo, icon_image=main_body_logo)
# st.sidebar.markdown("Hi!")


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

# Text input para o valor da coluna "Guia"
col_guia = st.text_input('Digite o valor para a coluna "Guia"')

# Date input para o intervalo de datas da coluna "Dt item"
date_range = st.date_input(
    "Selecione o intervalo de datas para a coluna 'Dt item'",
    value=(pd.to_datetime('2024-01-01').date(), pd.to_datetime('2024-12-31').date())
)

# Ler e filtrar o arquivo XLS
df_filtered = read_and_filter_xls(xls_file, column_names)

# Exibir o DataFrame filtrado se existir
if df_filtered is not None:
    st.write(f'Tabela filtrada pelos valores:')
    
    # Verificar se as colunas "Guia" e "Dt item" estão presentes no DataFrame
    guia_present = 'Guia' in df_filtered.columns
    dt_item_present = 'Dt item' in df_filtered.columns

    if guia_present and dt_item_present:
        # Converter a coluna "Dt item" para datetime
        df_filtered['Dt item'] = pd.to_datetime(df_filtered['Dt item'], errors='coerce').dt.date

        # Converter as datas selecionadas para datetime.date
        start_date = pd.to_datetime(date_range[0]).date()
        end_date = pd.to_datetime(date_range[1]).date()
        
        # Filtrar o DataFrame pelos valores digitados e intervalo de datas
        df_filtered = df_filtered[
            (df_filtered['Guia'].astype(str).str.contains(col_guia)) & 
            (df_filtered['Dt item'] >= start_date) & 
            (df_filtered['Dt item'] <= end_date)
        ]
        st.table(df_filtered)
    else:
        if not guia_present:
            st.warning('Coluna "Guia" não encontrada no DataFrame.')
        if not dt_item_present:
            st.warning('Coluna "Dt item" não encontrada no DataFrame.')
