import pandas as pd
import streamlit as st
from io import BytesIO

# Função para ler e filtrar o arquivo XLS
def read_and_filter_xls(xls_file, column_names, col_guia, start_date, end_date):
    try:
        # Ler o arquivo XLS e criar DataFrame
        df = pd.read_excel(xls_file)

        # Filtrar apenas as colunas especificadas
        df_filtered = df[column_names]

        # Verificar se as colunas "Guia" e "Dt item" estão presentes no DataFrame
        guia_present = 'Guia' in df_filtered.columns
        dt_item_present = 'Dt item' in df_filtered.columns

        if guia_present and dt_item_present:
            # Converter a coluna "Dt item" para datetime
            df_filtered['Dt item'] = pd.to_datetime(df_filtered['Dt item'], errors='coerce').dt.date

            # Filtrar o DataFrame pelos valores digitados e intervalo de datas
            df_filtered = df_filtered[
                (df_filtered['Guia'].astype(str).str.contains(col_guia)) & 
                (df_filtered['Dt item'] >= start_date) & 
                (df_filtered['Dt item'] <= end_date)
            ]
            return df_filtered
        else:
            if not guia_present:
                st.warning('Coluna "Guia" não encontrada no DataFrame.')
            if not dt_item_present:
                st.warning('Coluna "Dt item" não encontrada no DataFrame.')
            return None
    
    except FileNotFoundError:
        st.error(f"Arquivo não encontrado: {xls_file}")
        return None
    except Exception as e:
        st.error(f"Ocorreu um erro: {e}")
        return None

# Interface do Streamlit
st.image("LOGO.png", width=200)
st.title('Leitura e Filtro de Arquivo XLS')

# Upload de arquivo
uploaded_file = st.file_uploader("Escolha um arquivo XLS/XLSX")

# Se um arquivo for carregado
if uploaded_file is not None:
    # Text input para o valor da coluna "Guia"
    col_guia = st.text_input('Digite o valor para a coluna "Guia"')

    # Date input para o intervalo de datas da coluna "Dt item"
    date_range = st.date_input(
        "Selecione o intervalo de datas para a coluna 'Dt item'",
        value=(pd.to_datetime('2024-01-01').date(), pd.to_datetime('2024-12-31').date())
    )

    # Exibir o nome do arquivo e detalhes básicos
    st.write(f'Nome do arquivo: {uploaded_file.name}')
    st.write(f'Tamanho do arquivo: {uploaded_file.size} bytes')

    # Botão para processar o arquivo
    if st.button('Processar arquivo'):
        # Ler e filtrar o arquivo XLS se col_guia e data_range estiverem definidos
        if col_guia and date_range:
            column_names = ['Guia', 'Dt item']
            df_filtered = read_and_filter_xls(uploaded_file, column_names, col_guia, date_range[0], date_range[1])

            # Exibir o DataFrame filtrado se existir
            if df_filtered is not None:
                st.write(f'Tabela filtrada pelos valores:')
                st.table(df_filtered)
            if st.button('Exportar para Excel'):
                # Salvar o DataFrame filtrado em um arquivo Excel
                file_name = f'resultado_filtrado_{col_guia}.xlsx'  # Nome do arquivo de saída
                df_filtered.to_excel(file_name, index=False)
                st.success(f'Arquivo salvo com sucesso: {file_name}')