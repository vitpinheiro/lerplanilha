import pandas as pd
import streamlit as st
from io import BytesIO
import openpyxl
from datetime import datetime

# Função para ler e filtrar o arquivo XLS
def read_and_filter_xls(xls_file, column_names, col_guia=None, date_range=None):
    try:
        # Ler o arquivo XLS e criar DataFrame
        df = pd.read_excel(xls_file)

        # Filtrar apenas as colunas especificadas
        df_filtered = df[column_names]

        # Aplicar filtro por "Guia" se col_guia estiver definido
        if col_guia:
            df_filtered = df_filtered[df_filtered['Guia'].astype(str).str.contains(col_guia)]

        # Aplicar filtro por "Dt item" se date_range estiver definido
        if date_range:
            start_date = pd.to_datetime(date_range[0]).date()
            end_date = pd.to_datetime(date_range[1]).date()

            # Converter a coluna "Dt item" para datetime.date
            df_filtered['Dt item'] = pd.to_datetime(df_filtered['Dt item'], errors='coerce').dt.date

            df_filtered = df_filtered[(df_filtered['Dt item'] >= start_date) & (df_filtered['Dt item'] <= end_date)]

        return df_filtered
    
    except FileNotFoundError:
        st.error(f"Arquivo não encontrado: {xls_file}")
        return None
    except Exception as e:
        st.error(f"Ocorreu um erro: {e}")
        return None

# Interface do Streamlit
st.image("LOGO.png", width=150)
st.title('Leitura e Filtro de Arquivo XLS')

# Upload de arquivo
uploaded_file = st.file_uploader("Escolha um arquivo XLS/XLSX")

column_names = ['Guia', 'Dt item']

# Se um arquivo for carregado
if uploaded_file is not None:
    # Checkbox e input para filtro de "Guia"
    guia = st.checkbox("Filtro Guia", value=True)
    if guia:
        col_guia = st.text_input('Digite o valor para a coluna "Guia"')

    # Checkbox e input para filtro de data
    data = st.checkbox("Filtro Data", value=True)
    if data:
        date_range = st.date_input(
            "Selecione o intervalo de datas para a coluna 'Dt item'",
            value=(pd.to_datetime('2024-01-01').date(), pd.to_datetime('2024-12-31').date())
        )

    # Botão para aplicar filtros e exibir tabela filtrada
    if st.button('Aplicar Filtros'):
        df_filtered = read_and_filter_xls(uploaded_file, column_names, col_guia if guia else None, date_range if data else None)
        
        if df_filtered is not None:
            st.write('Tabela filtrada pelos valores selecionados:')
            st.table(df_filtered)

            # Botão para exportar para Excel
            output = BytesIO()
            df_filtered.to_excel(output, index=False)
            output.seek(0)

            st.download_button(
                label="Baixar arquivo Excel",
                data=output,
                file_name=f"resultado_filtrado_{datetime.today().strftime('%Y-%m-%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    # Exibir o nome do arquivo e detalhes básicos
    st.write(f'Nome do arquivo: {uploaded_file.name}')
    st.write(f'Tamanho do arquivo: {uploaded_file.size} bytes')
