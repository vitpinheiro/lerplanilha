import pandas as pd
import streamlit as st
from io import BytesIO
from datetime import datetime

def read_and_filter_xls(xls_file, column_names, guide_values=None, date_range=None):
    try:
        df = pd.read_excel(xls_file)
        df_filtered = df[column_names]

        if guide_values:
            # Remove pontos ao converter os valores para strings
            df_filtered['Guia'] = df_filtered['Guia'].apply(lambda x: str(x).replace('.', ''))
            guide_values = [str(value).replace('.', '') for value in guide_values]
            df_filtered = df_filtered[df_filtered['Guia'].isin(guide_values)]

        if date_range:
            start_date = pd.to_datetime(date_range[0]).date()
            end_date = pd.to_datetime(date_range[1]).date()
            df_filtered['Dt item'] = pd.to_datetime(df_filtered['Dt item'], errors='coerce').dt.date
            df_filtered = df_filtered[(df_filtered['Dt item'] >= start_date) & (df_filtered['Dt item'] <= end_date)]

        return df_filtered
    except FileNotFoundError:
        st.error(f"Arquivo não encontrado: {xls_file}")
        return None
    except Exception as e:
        st.error(f"Ocorreu um erro: {e}")
        return None

def page_tratamento():
    st.image("LOGO.png", width=150)
    st.write("TRATAMENTO")
    st.header('Leitura e Filtro de Arquivo XLS')

    uploaded_file = st.file_uploader("Escolha um arquivo XLS/XLSX")

    column_names = ['Guia', 'Dt item']
    guide_values = []

    if uploaded_file is not None:
        guia = st.checkbox("Filtro Guia", value=True)
        if guia:
            guide_values = st.text_area('Digite os valores para a coluna "Guia" (separados por vírgulas)').split(',')

        data = st.checkbox("Filtro Data", value=True)
        date_range = None
        if data:
            date_range = st.date_input(
                "Selecione o intervalo de datas para a coluna 'Dt item'",
                value=(pd.to_datetime('2024-01-01').date(), pd.to_datetime('2024-12-31').date())
            )

        if st.button('Aplicar Filtros'):
            df_filtered = read_and_filter_xls(uploaded_file, column_names, guide_values if guia else None, date_range if data else None)
            if df_filtered is not None:
                st.write('Tabela filtrada pelos valores selecionados:')
                st.dataframe(df_filtered)
                output = BytesIO()
                df_filtered.to_excel(output, index=False)
                output.seek(0)
                st.download_button(
                    label="Baixar arquivo Excel",
                    data=output,
                    file_name=f"resultado_filtrado_{datetime.today().strftime('%Y-%m-%d')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

        st.write(f'Nome do arquivo: {uploaded_file.name}')
        st.write(f'Tamanho do arquivo: {uploaded_file.size} bytes')
    else:
        st.write("Por favor, faça o upload de um arquivo XLS/XLSX.")

    st.header('Upload e Filtragem do Arquivo ATENDIMENTOS')
    uploaded_file2 = st.file_uploader("Escolha o arquivo ATENDIMENTOS.xls", key="atendimentos")

    if uploaded_file2 is not None:
        if guide_values:
            df = pd.read_excel(uploaded_file2)
            # Remova pontos dos valores nas colunas relevantes
            df['GUIA_ATENDIMENTO'] = df['GUIA_ATENDIMENTO'].apply(lambda x: str(x).replace('.', ''))
            df['GIH_NUMERO'] = df['GIH_NUMERO'].apply(lambda x: str(x).replace('.', ''))
            guide_values = [str(value).replace('.', '') for value in guide_values]

            df_filtered_guia = df[df['GUIA_ATENDIMENTO'].isin(guide_values) | df['GIH_NUMERO'].isin(guide_values)]

            df_filtered_guia = df_filtered_guia[df_filtered_guia['CTH_NUM'] == 0]
            df_filtered_guia = df_filtered_guia[pd.notna(df_filtered_guia['FAT_NUM'])]
            df_filtered_guia = df_filtered_guia[df_filtered_guia['GUIA_ATENDIMENTO'] == df_filtered_guia['GIH_NUMERO']]
            # Mostra as colunas filtradas de interesse
            df_filtered2 = df_filtered_guia[['CTH_NUM', 'GUIA_ATENDIMENTO', 'GIH_NUMERO', 'FAT_NUM']]
            st.dataframe(df_filtered2)

            output2 = BytesIO()
            df_filtered2.to_excel(output2, index=False)
            output2.seek(0)
            st.download_button(
                label="Baixar arquivo Excel",
                data=output2,
                file_name=f"resultado_atendimentos_filtrado_{datetime.today().strftime('%Y-%m-%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.write("Por favor, insira um valor para a coluna 'Guia' no filtro acima.")
    else:
        st.write("Por favor, faça o upload do arquivo ATENDIMENTOS v3.xls.")

page_tratamento()
