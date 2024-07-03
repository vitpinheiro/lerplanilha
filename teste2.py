import pandas as pd
import streamlit as st
from io import BytesIO
from datetime import datetime


def read_and_filter_xls(file, column_names, guide_values, date_range):
    df = pd.read_excel(file)
    if 'Guia' in column_names and guide_values:
        df = df[df['Guia'].astype(str).isin(guide_values)]
    if 'Dt item' in column_names and date_range:
        df['Dt item'] = pd.to_datetime(df['Dt item'], dayfirst=True, errors='coerce')
        df = df[(df['Dt item'] >= pd.to_datetime(date_range[0])) & (df['Dt item'] <= pd.to_datetime(date_range[1]))]
    return df

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
                value=(datetime(2024, 1, 1).date(), datetime(2024, 12, 31).date())
            )

        if st.button('Aplicar Filtros'):
            guide_values_to_use = guide_values if guia else None
            date_range_to_use = date_range if data else None

            df_filtered = read_and_filter_xls(uploaded_file, column_names, guide_values_to_use, date_range_to_use)
            if df_filtered is not None:
                st.write('Tabela filtrada pelos valores selecionados:')
                st.dataframe(df_filtered[['Guia', 'Dt item']])

                min_date = df_filtered['Dt item'].min()
                st.write(f"A menor data encontrada é: {min_date}")

                df_filtered_by_min_date = df_filtered[df_filtered['Dt item'] == min_date][['Guia', 'Dt item']]
                st.write('Tabela filtrada pela menor data:')
                st.dataframe(df_filtered_by_min_date)

                output = BytesIO()
                df_filtered_by_min_date.to_excel(output, index=False)
                output.seek(0)
                st.download_button(
                    label="Baixar arquivo Excel",
                    data=output,
                    file_name=f"resultado_demonstrativo_{datetime.today().strftime('%Y-%m-%d')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

      
    else:
        st.write("Por favor, faça o upload de um arquivo XLS/XLSX.")

    st.header('Upload e Filtragem do Arquivo ATENDIMENTOS')

    uploaded_file2 = st.file_uploader("Escolha o arquivo ATENDIMENTOS.xls", key="atendimentos")

    if uploaded_file2 is not None:
        df = pd.read_excel(uploaded_file2)

        df['GUIA_ATENDIMENTO'] = df['GUIA_ATENDIMENTO'].astype(str).str.replace('.', '')
        df['GUIA_CONTA'] = df['GUIA_CONTA'].astype(str).str.replace('.', '')
        df['GIH_NUMERO'] = df['GIH_NUMERO'].astype(str).str.replace('.', '')

        if 'df_filtered' in locals() and not df_filtered.empty:
            min_date = df_filtered['Dt item'].min()

            df['CTH_DTHR_INI'] = pd.to_datetime(df['CTH_DTHR_INI'], errors='coerce')
            df['CTH_DTHR_FIN'] = pd.to_datetime(df['CTH_DTHR_FIN'], errors='coerce')

            min_date_timestamp = min_date.timestamp()

            df = df[
                (df['CTH_DTHR_INI'].apply(lambda x: x.timestamp() if pd.notnull(x) else None) <= min_date_timestamp) & 
                (min_date_timestamp <= df['CTH_DTHR_FIN'].apply(lambda x: x.timestamp() if pd.notnull(x) else None))
            ]
           
            df = df[df['GUIA_ATENDIMENTO'] == df['GIH_NUMERO']]

            df_filtered2 = df[['GUIA_ATENDIMENTO','HSP_NUM', 'HSP_PAC', 'CTH_NUM', 'FAT_SERIE', 'FAT_NUM', 'NFS_SERIE', 'NFS_NUMERO', 'CTH_DTHR_INI', 'CTH_DTHR_FIN']]
            df_filtered2['NFS_NUMERO'] = df_filtered2['NFS_NUMERO'].astype(str)
            df_filtered2['HSP_PAC'] = df_filtered2['HSP_PAC'].astype(str)
            df_filtered2['FAT_NUM'] = df_filtered2['FAT_NUM'].astype(str)
           
            st.dataframe(df_filtered2.rename(columns={
                'GUIA_ATENDIMENTO': 'Guia',
                'HSP_NUM': 'IH',
                'HSP_PAC': 'Registro',
                'CTH_NUM': 'Conta',
                'FAT_SERIE': 'Pre. S',
                'FAT_NUM': 'Pre. Num',
                'NFS_SERIE': 'Fat. S',
                'NFS_NUMERO': 'Fat. Num',
                'CTH_DTHR_INI': 'DT INI',
                'CTH_DTHR_FIN': 'DT FIM'
            }))
            output2 = BytesIO()
            df_filtered2.to_excel(output2, index=False, header=[
                'Guia', 'IH', 'Registro', 'Conta', 'Pre. S', 'Pre. Num', 'Fat. S', 'Fat. Num', 'DT INI', 'DT FIM'
            ])  # Usar header para definir os nomes das colunas no arquivo Excel
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
                st.dataframe(df_filtered[['Guia', 'Dt item']])
            

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

