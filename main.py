import pandas as pd
import streamlit as st
from io import BytesIO
from datetime import datetime


def ler_e_filtrar_xls(file, nomes_colunas, valores_guias, intervalo_data):
    # df é a variável que armazena o dataframe lido a partir do arquivo excel usando a função pd.read_excel()
    df = pd.read_excel(file)
    if 'Guia' in nomes_colunas and valores_guias:
        df = df[df['Guia'].astype(str).isin(valores_guias)]
    if 'Dt item' in nomes_colunas and intervalo_data:
        df['Dt item'] = pd.to_datetime(df['Dt item'], dayfirst=True, errors='coerce')
        df = df[(df['Dt item'] >= pd.to_datetime(intervalo_data[0])) & (df['Dt item'] <= pd.to_datetime(intervalo_data[1]))]
    return df

def main_page():
    st.image("LOGO.png", width=150)
    st.header('Filtragem de dados sobre Internação')

    arquivo_carregado = st.file_uploader("Escolha o arquivo 'Demonstrativo' em formato xls")

    # st.markdown('<p class="primary-color">Este é um exemplo de texto com a cor primária.</p>', unsafe_allow_html=True)

    nomes_colunas = ['Guia', 'Dt item']
    valores_guias = []

    if arquivo_carregado is not None:
        guia = st.checkbox("Filtro Guia", value=False)
        if guia:
            valores_guias = st.text_input('Digite os valores das guias separados por vírgulas').split(',')

        data = st.checkbox("Filtro Data", value=True)
        intervalo_data = None
        if data:
            intervalo_data = st.date_input(
                "Selecione o intervalo de datas",
                value=(datetime(2024, 1, 1).date(), datetime(2024, 12, 31).date())
            )

        if st.button('Aplicar Filtros'):
            guias_selecionadas = valores_guias if guia else None
            intervalodata_selecionado = intervalo_data if data else None

            df_filtrado = ler_e_filtrar_xls(arquivo_carregado, nomes_colunas, guias_selecionadas, intervalodata_selecionado)
            if df_filtrado is not None:
             
                if df_filtrado.empty:
                    st.markdown("<h3 style='color: red;'>Linha não encontrada</h3>", unsafe_allow_html=True)
                else:
                    st.write('Tabela filtrada pelos valores selecionados:')
                    st.dataframe(df_filtrado[['Guia', 'Dt item']])
               

                    min_date = df_filtrado['Dt item'].min()
                    min_date2 = pd.to_datetime(min_date, format= "%Y-%m-%d %H:%M:%S")
                    
                    st.write(f"A menor data encontrada é: {min_date2}")

                    # df_filtrado_by_min_date = df_filtrado[df_filtrado['Dt item'] == min_date][['Guia', 'Dt item']]
                # st.write('Tabela filtrada pela menor data:')
                # st.dataframe(df_filtrado_by_min_date)
      
    else:
        st.write("Por favor, faça o upload de um arquivo XLS/XLSX.")

    st.header('Upload e Filtragem do Arquivo ATENDIMENTOS')

    arquivo_carregado2 = st.file_uploader("Escolha o arquivo 'Atendimentos' no formato xls", key="atendimentos")

    if arquivo_carregado2 is not None:
        df = pd.read_excel(arquivo_carregado2)
        df['Índice Original'] = df.index
        df_filtrado_guia = df[
                df['GUIA_ATENDIMENTO'].isin(df.index) |
                df['GUIA_CONTA'].isin(df.index) |
                df['GIH_NUMERO'].isin(df.index)
            ]

        df['GUIA_ATENDIMENTO'] = df['GUIA_ATENDIMENTO'].astype(str).str.replace('.', '')
        df['GUIA_CONTA'] = df['GUIA_CONTA'].astype(str).str.replace('.', '')
        df['GIH_NUMERO'] = df['GIH_NUMERO'].astype(str).str.replace('.', '')

        if valores_guias:
            df_filtrado_guia = df[df['GUIA_ATENDIMENTO'].isin(valores_guias) | df['GUIA_CONTA'].isin(valores_guias)]

        else:
            df_filtrado_guia = df.copy()

        if 'df_filtrado'in locals() and not df_filtrado.empty:
            
            min_date = df_filtrado['Dt item'].min()
            min_date2 = pd.to_datetime(min_date, format="%Y-%m-%d %H:%M:%S")
        

            df_filtrado_guia['CTH_DTHR_INI'] = pd.to_datetime(df_filtrado_guia['CTH_DTHR_INI'], errors='coerce')
            df_filtrado_guia['CTH_DTHR_FIN'] = pd.to_datetime(df_filtrado_guia['CTH_DTHR_FIN'], errors='coerce')

            # st.write(df_filtrado_guia['CTH_DTHR_INI'])
            # st.write(df_filtrado_guia['CTH_DTHR_FIN'])


            if len(df_filtrado_guia) == 1:
                df_filtrado2 = df_filtrado_guia
            else:   
                df_filtrado_guia = df_filtrado_guia.loc[
                    (df_filtrado_guia['CTH_DTHR_INI'] <= min_date2) &
                    (min_date2 <= df_filtrado_guia['CTH_DTHR_FIN'])
                ]

            
            df_filtrado2 = df_filtrado_guia[df_filtrado_guia['GUIA_ATENDIMENTO'] == df_filtrado_guia['GIH_NUMERO']]
            df_filtrado2 = df_filtrado2[['GUIA_ATENDIMENTO','GUIA_CONTA','HSP_NUM', 'HSP_PAC', 'CTH_NUM', 'FAT_SERIE', 'FAT_NUM', 'NFS_SERIE', 'NFS_NUMERO', 'CTH_DTHR_INI', 'CTH_DTHR_FIN']]
            df_filtrado2['NFS_NUMERO'] = df_filtrado2['NFS_NUMERO'].astype(str)
            df_filtrado2['HSP_PAC'] = df_filtrado2['HSP_PAC'].astype(str)
            df_filtrado2['FAT_NUM'] = df_filtrado2['FAT_NUM'].astype(str)
            df_filtrado2 = df_filtrado2.rename(columns={'HSP_NUM':'IH', 'HSP_PAC':'REGISTRO', 'CTH_NUM':'CONTA', 'FAT_SERIE':'PRE.S', 'FAT_NUM':'PRE.NUM', 'NFS_SERIE':'FAT.S', 'NFS_NUMERO':'FAT.NUM', 'CTH_DTHR_INI':'DATA_INICIO', 'CTH_DTHR_FIN':'DATA_FIM'})
       
            # st.dataframe(df_filtrado2)
            
            # Merge para encontrar apenas as linhas em comum com 'GUIA_ATENDIMENTO'
            result = pd.merge(df_filtrado[['Guia', 'Dt item']], df_filtrado2, left_on='Guia', right_on='GUIA_ATENDIMENTO', how='inner')
            
            
            result.drop_duplicates(subset=['Guia'], keep='first', inplace=True)

            st.dataframe(result)

            output2 = BytesIO()
            result.to_excel(output2, index=False)
            output2.seek(0)
            st.download_button(
                label="Baixar arquivo Excel",
                data=output2,
                file_name=f"resultado_atendimentos_filtrado_{datetime.today().strftime('%Y-%m-%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.markdown(
            "<h3 style='color: red; font-weight: bold;'>Por favor, primeiro clique em aplicar filtro</h3>",
            unsafe_allow_html=True
            )
            
    else:
        st.write("Por favor, faça o upload do arquivo 'Atendimentos'!")

def page_tratamento():
    st.image("LOGO.png", width=150)
    st.header('Filtragem de dados sobre Tratamento')

    arquivo_carregado = st.file_uploader("Escolha o arquivo 'Demonstrativo' em formato xls")

    nomes_colunas = ['Guia', 'Dt item']
    valores_guias = []

    if arquivo_carregado is not None:
        guia = st.checkbox("Filtro Guia", value=False)
        if guia:
            valores_guias = st.text_input('Digite os valores das guias separados por vírgulas').split(',')

        data = st.checkbox("Filtro Data", value=True)
        intervalo_data = None
        if data:
            intervalo_data = st.date_input(
                "Selecione o intervalo de datas",
                value=(pd.to_datetime('2024-01-01').date(), pd.to_datetime('2024-12-31').date())
            )

        if st.button('Aplicar Filtros'):
            guias_selecionadas = valores_guias if guia else None
            intervalodata_selecionado = intervalo_data if data else None

            df_filtrado = ler_e_filtrar_xls(arquivo_carregado, nomes_colunas, guias_selecionadas, intervalodata_selecionado)
            if df_filtrado is not None:
                st.write('Tabela filtrada pelos valores selecionados:')
                st.dataframe(df_filtrado[['Guia', 'Dt item']])
                
                min_date = df_filtrado['Dt item'].min()
                st.write(f"A menor data encontrada é: {min_date}")

                df_filtrado_by_min_date = df_filtrado[df_filtrado['Dt item'] == min_date][['Guia', 'Dt item']]
                st.write('Tabela filtrada pela menor data:')
                st.dataframe(df_filtrado_by_min_date)

        st.write(f'Nome do arquivo: {arquivo_carregado.name}')
        st.write(f'Tamanho do arquivo: {arquivo_carregado.size} bytes')
    else:
        st.write("Por favor, faça o upload de um arquivo XLS/XLSX.")

    st.header('Upload e Filtragem do Arquivo ATENDIMENTOS')
    arquivo_carregado2 = st.file_uploader("Escolha o arquivo 'Atendimentos' no formato xls", key="atendimentos")

    if arquivo_carregado2 is not None:
        df = pd.read_excel(arquivo_carregado2)
        
        # Remover pontos dos valores nas colunas relevantes
        df['GUIA_ATENDIMENTO'] = df['GUIA_ATENDIMENTO'].apply(lambda x: str(x).replace('.', ''))
        df['GIH_NUMERO'] = df['GIH_NUMERO'].apply(lambda x: str(x).replace('.', ''))
        valores_guias = [str(value).replace('.', '') for value in valores_guias]

        if valores_guias:
            df_filtrado_guia = df[df['GUIA_ATENDIMENTO'].isin(valores_guias) | df['GIH_NUMERO'].isin(valores_guias)]
        else:
            df_filtrado_guia = df.copy()

        if 'guias_selecionadas' in locals() and 'df_filtrado_guia' in locals() and 'df_filtrado' in locals():

        

            df_filtrado_guia = df_filtrado_guia[df_filtrado_guia['CTH_NUM'] == 0]
            df_filtrado_guia = df_filtrado_guia[df_filtrado_guia['GUIA_ATENDIMENTO'] == df_filtrado_guia['GIH_NUMERO']]
            df_filtrado2 = df_filtrado_guia[['GUIA_ATENDIMENTO', 'GUIA_CONTA', 'HSP_NUM', 'HSP_PAC', 'CTH_NUM', 'FAT_SERIE', 'FAT_NUM', 'NFS_SERIE', 'NFS_NUMERO']]
            df_filtrado2['NFS_NUMERO'] = df_filtrado2['NFS_NUMERO'].astype(str)
            df_filtrado2 = df_filtrado2.rename(columns={'HSP_NUM':'IH', 'HSP_PAC':'REGISTRO', 'CTH_NUM':'CONTA', 'FAT_SERIE':'PRE.S', 'FAT_NUM':'PRE.NUM', 'NFS_SERIE':'FAT.S', 'NFS_NUMERO':'FAT.NUM'})
            result = pd.merge(df_filtrado[['Guia', 'Dt item']], df_filtrado2, left_on='Guia', right_on='GUIA_ATENDIMENTO', how='inner')
                
                
            result.drop_duplicates(subset=['Guia'], keep='first', inplace=True)

            st.dataframe(result)
        
            output2 = BytesIO()
            result.to_excel(output2, index=False)                   
            output2.seek(0)
            st.download_button(
                label="Baixar arquivo Excel",
                data=output2,
                file_name=f"resultado_atendimentos_filtrado_{datetime.today().strftime('%Y-%m-%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            ) 
        else:
            st.markdown(
            "<h3 style='color: red; font-weight: bold;'>Por favor, primeiro clique em aplicar filtro</h3>",
            unsafe_allow_html=True
            )
    else:
        st.write("Por favor, faça o upload do arquivo ATENDIMENTOS v3.xls.")

# Navegação entre páginas
st.sidebar.title("Navegação")
page = st.sidebar.radio("", ["INTERNAÇÃO", "TRATAMENTO"])

if page == "INTERNAÇÃO":
    main_page()
else:
    page_tratamento()
