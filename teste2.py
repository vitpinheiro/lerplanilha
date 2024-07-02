import pandas as pd
import streamlit as st
from io import BytesIO
from datetime import datetime


# Função para ler e filtrar o arquivo XLS
def read_and_filter_xls(xls_file, column_names, guide_values=None, date_range=None):
    try:
        df = pd.read_excel(xls_file)
        df_filtered = df[column_names]

        if guide_values:
            df_filtered = df_filtered[df_filtered['Guia'].astype(str).isin(guide_values)]

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

def main_page():
    st.image("LOGO.png", width=150)
    st.write("INTERNAÇÃO")
    st.header('Leitura e Filtro de Arquivo XLS')

    uploaded_file = st.file_uploader("Escolha um arquivo XLS/XLSX")

    column_names = ['Guia', 'Dt item']
    guide_values = []

    if uploaded_file is not None:
        guia = st.checkbox("Filtro Guia", value=True)
        if guia:
            guide_values = st.text_input('Digite os valores para a coluna "Guia" (separados por vírgulas)').split(',')

        data = st.checkbox("Filtro Data", value=True)
        date_range = None
        if data:
            date_range = st.date_input(
                "Selecione o intervalo de datas para a coluna 'Dt item'",
                value=(pd.to_datetime('2024-01-01').date(), pd.to_datetime('2024-12-31').date())
            )

        if st.button('Aplicar Filtros'):
            # Ajustar os parâmetros para a função de leitura e filtragem
            guide_values_to_use = guide_values if guia else None
            date_range_to_use = date_range if data else None

            df_filtered = read_and_filter_xls(uploaded_file, column_names, guide_values_to_use, date_range_to_use)
            if df_filtered is not None:
                st.write('Tabela filtrada pelos valores selecionados:')
                st.dataframe(df_filtered)
                # min_date = df_filtered['Dt item'].min()
                # max_date = df_filtered['Dt item'].max()
                # st.write(f"A menor data encontrada é: {min_date}")
                # st.write(f"A menor data encontrada é: {max_date}")

                # Aplicar um novo filtro baseado na menor data encontrada
                # df_filtered = df_filtered[df_filtered['Dt item']]
                # st.write('Tabela filtrada pela menor data:')
                # st.dataframe(df_filtered)
                output = BytesIO()
                df_filtered.to_excel(output, index=False)
                output.seek(0)
                st.download_button(
                    label="Baixar arquivo Excel",
                    data=output,
                    file_name=f"resultado_demonstrativo_{datetime.today().strftime('%Y-%m-%d')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

                # Agora, você pode continuar com o processamento usando df_filtered

        st.write(f'Nome do arquivo: {uploaded_file.name}')
        st.write(f'Tamanho do arquivo: {uploaded_file.size} bytes')
    else:
        st.write("Por favor, faça o upload de um arquivo XLS/XLSX.")

    st.header('Upload e Filtragem do Arquivo ATENDIMENTOS')

    uploaded_file2 = st.file_uploader("Escolha o arquivo ATENDIMENTOS.xls", key="atendimentos")

    if uploaded_file2 is not None:
        # Leitura do arquivo ATENDIMENTOS
        df = pd.read_excel(uploaded_file2)

        # Remover pontos dos valores nas colunas relevantes
        df['GUIA_ATENDIMENTO'] = df['GUIA_ATENDIMENTO'].astype(str).str.replace('.', '')
        df['GUIA_CONTA'] = df['GUIA_CONTA'].astype(str).str.replace('.', '')
        df['GIH_NUMERO'] = df['GIH_NUMERO'].astype(str).str.replace('.', '')

        if guide_values:
            df_filtered_guia = df[df['GUIA_ATENDIMENTO'].isin(guide_values) | df['GUIA_CONTA'].isin(guide_values) | df['GIH_NUMERO'].isin(guide_values)]
        else:
            df_filtered_guia = df.copy()

        if 'df_filtered' in locals():
            min_date = df_filtered['Dt item']
            
            
            df_filtered_guia['CTH_DTHR_INI'] = pd.to_datetime(df_filtered_guia['CTH_DTHR_INI']).dt.date
            df_filtered_guia['CTH_DTHR_FIN'] = pd.to_datetime(df_filtered_guia['CTH_DTHR_FIN']).dt.date

            
            df_filtered_guia = df_filtered_guia[
                (df_filtered_guia['CTH_DTHR_INI'] <= min_date) & (min_date <= df_filtered_guia['CTH_DTHR_FIN'])
            ]
           
            
            df_filtered_guia = df_filtered_guia[df_filtered_guia['GUIA_ATENDIMENTO'] == df_filtered_guia['GIH_NUMERO']]

            
            df_filtered2 = df_filtered_guia[['HSP_NUM', 'HSP_PAC', 'CTH_NUM', 'FAT_SERIE', 'FAT_NUM', 'NFS_SERIE', 'NFS_NUMERO','CTH_DTHR_INI','CTH_DTHR_FIN']]
            df_filtered2['NFS_NUMERO'] = df_filtered2['NFS_NUMERO'].astype(str)
            st.dataframe(df_filtered2)

            # Criar botão de download para o arquivo Excel filtrado
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
            st.write("Por favor, primeiro aplique os filtros no arquivo XLS/XLSX.")

    else:
        st.write("Por favor, faça o upload do arquivo ATENDIMENTOS v3.xls.")

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
            guide_values = st.text_input('Digite os valores para a coluna "Guia" (separados por vírgulas)').split(',')

        data = st.checkbox("Filtro Data", value=True)
        date_range = None
        if data:
            date_range = st.date_input(
                "Selecione o intervalo de datas para a coluna 'Dt item'",
                value=(pd.to_datetime('2024-01-01').date(), pd.to_datetime('2024-12-31').date())
            )

        if st.button('Aplicar Filtros'):
            guide_values_to_use = guide_values if guia else None
            date_range_to_use = date_range if data else None

            df_filtered = read_and_filter_xls(uploaded_file, column_names, guide_values_to_use, date_range_to_use)
            if df_filtered is not None:
                st.write('Tabela filtrada pelos valores selecionados:')
                st.dataframe(df_filtered)
                output = BytesIO()
                df_filtered.to_excel(output, index=False)
                output.seek(0)
                st.download_button(
                    label="Baixar arquivo Excel",
                    data=output,
                    file_name=f"resultado_ATENDIMENTO_{datetime.today().strftime('%Y-%m-%d')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

        st.write(f'Nome do arquivo: {uploaded_file.name}')
        st.write(f'Tamanho do arquivo: {uploaded_file.size} bytes')
    else:
        st.write("Por favor, faça o upload de um arquivo XLS/XLSX.")

    st.header('Upload e Filtragem do Arquivo ATENDIMENTOS')
    uploaded_file2 = st.file_uploader("Escolha o arquivo ATENDIMENTOS.xls", key="atendimentos")

    if uploaded_file2 is not None:
        df = pd.read_excel(uploaded_file2)
        
        # Remover pontos dos valores nas colunas relevantes
        df['GUIA_ATENDIMENTO'] = df['GUIA_ATENDIMENTO'].apply(lambda x: str(x).replace('.', ''))
        df['GIH_NUMERO'] = df['GIH_NUMERO'].apply(lambda x: str(x).replace('.', ''))
        guide_values = [str(value).replace('.', '') for value in guide_values]

        if guide_values:
            df_filtered_guia = df[df['GUIA_ATENDIMENTO'].isin(guide_values) | df['GIH_NUMERO'].isin(guide_values)]
        else:
            df_filtered_guia = df.copy()

        df_filtered_guia = df_filtered_guia[df_filtered_guia['CTH_NUM'] == 0]
        df_filtered_guia = df_filtered_guia[pd.notna(df_filtered_guia['FAT_NUM'])]
        df_filtered_guia = df_filtered_guia[df_filtered_guia['GUIA_ATENDIMENTO'] == df_filtered_guia['GIH_NUMERO']]
        df_filtered2 = df_filtered_guia[['HSP_NUM', 'HSP_PAC', 'CTH_NUM', 'FAT_SERIE', 'FAT_NUM', 'NFS_SERIE', 'NFS_NUMERO']]
        df_filtered2['NFS_NUMERO'] = df_filtered2['NFS_NUMERO'].astype(str)

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
        st.write("Por favor, faça o upload do arquivo ATENDIMENTOS v3.xls.")

# Navegação entre páginas
st.sidebar.title("Navegação")
page = st.sidebar.radio("Ir para", ["INTERNAÇÃO", "TRATAMENTO"])

if page == "INTERNAÇÃO":
    main_page()
else:
    page_tratamento()

