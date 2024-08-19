import pandas as pd
import streamlit as st
from io import BytesIO
from datetime import datetime

def ler_e_filtrar_xls(file, nomes_colunas, valores_guias, intervalo_data):
    try:
        file.seek(0)
        df = pd.read_excel(file, engine='xlrd')
        
        if 'Guia' in df.columns:
            # Convertendo a coluna 'Guia' para numérico, ignorando valores não numéricos
            df['Guia'] = pd.to_numeric(df['Guia'], errors='coerce')
            df = df.dropna(subset=['Guia'])
            df['Guia'] = df['Guia'].astype(int)
            df.reset_index(drop=True, inplace=True)
        else:
            raise ValueError("A coluna 'Guia' não está presente no DataFrame.")

        if 'Guia' in nomes_colunas and valores_guias:
            # Converte os valores das guias para numérico, removendo possíveis espaços e tratando valores vazios
            valores_guias = [int(guia.strip()) for guia in valores_guias if guia.strip().isdigit()]
            df = df[df['Guia'].isin(valores_guias)]
        
        if 'Dt item' in nomes_colunas and intervalo_data:
            df['Dt item'] = pd.to_datetime(df['Dt item'], dayfirst=True, errors='coerce')
            df = df[(df['Dt item'] >= pd.to_datetime(intervalo_data[0])) & (df['Dt item'] <= pd.to_datetime(intervalo_data[1]))]
        
        return df
    
    except Exception as e:
        st.error(f"Ocorreu um erro ao processar o arquivo: {e}")
        return None

def main_page():
    st.image("LOGO.png", width=150)
    st.header('Filtragem de dados sobre Internação')
    
    # Carregamento do arquivo 'Demonstrativo'
    arquivo_demonstrativo = st.file_uploader("Escolha o arquivo 'Demonstrativo' em formato xls")
    nomes_colunas_guias = ['Guia', 'Dt item']
    valores_guias = []

    if arquivo_demonstrativo is not None:
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

        # Aplicando os filtros
        df_filtrado = ler_e_filtrar_xls(arquivo_demonstrativo, nomes_colunas_guias, valores_guias if guia else None, intervalo_data if data else None)

        if df_filtrado is not None:
            if df_filtrado.empty:
                st.markdown("<h3 style='color: red;'>Resultados não encontrados</h3>", unsafe_allow_html=True)
            else:
                st.write('Tabela filtrada pelos valores selecionados:')
                df_filtrado['Guia'] = df_filtrado['Guia'].astype(str).str.replace('.', '')
                st.dataframe(df_filtrado[['Guia', 'Dt item']])
    else:
        st.warning("Por favor, carregue o arquivo 'Demonstrativo'.")

    # Carregamento do arquivo 'Atendimentos'
    arquivo_atendimentos = st.file_uploader("Escolha o arquivo 'Atendimentos' em formato xls")
    
     
    if arquivo_demonstrativo is not None and arquivo_atendimentos is not None:
        df_demonstrativo = pd.read_excel(arquivo_demonstrativo, engine='xlrd')
        df_demonstrativo = df_demonstrativo[nomes_colunas_guias]
        df_demonstrativo = df_demonstrativo.astype(str)
        df_demonstrativo = df_demonstrativo.rename(columns={'Guia':'GUIA_ATENDIMENTO', 'Dt item':'DATA_GUIAS'})
        # df_demonstrativo['DATA_GUIAS'] = pd.to_datetime(df_demonstrativo['DATA_GUIAS'], format='%d/%m/%Y').dt.strftime('%d/%m/%Y')
        
        df_atendimentos = pd.read_excel(arquivo_atendimentos)
        df_atendimentos = df_atendimentos.astype(str)
        
        if valores_guias:
            valores_guias = [guia.strip() for guia in valores_guias if guia.strip().isdigit()]
            df_atendimentos = df_atendimentos[df_atendimentos['GUIA_ATENDIMENTO'].isin(valores_guias)]
        df_atendimentos['CTH_DTHR_INI'] = pd.to_datetime(df_atendimentos['CTH_DTHR_INI'], format='%Y-%m-%d %H:%M:%S.%f').dt.strftime('%d/%m/%Y')
        df_atendimentos['CTH_DTHR_FIN'] = pd.to_datetime(df_atendimentos['CTH_DTHR_FIN'], format='%Y-%m-%d %H:%M:%S.%f').dt.strftime('%d/%m/%Y')
        
        merge_df = pd.merge(df_demonstrativo, df_atendimentos, on='GUIA_ATENDIMENTO')
        df_filtrado_periodo = merge_df[(merge_df['DATA_GUIAS'] >= merge_df['CTH_DTHR_INI']) & (merge_df['DATA_GUIAS'] <= merge_df['CTH_DTHR_FIN'])]
        df_filtrado_periodo = df_filtrado_periodo.reset_index(drop=True)
        
        df_internacao = df_filtrado_periodo[df_filtrado_periodo['HSP_TRAT_INT'] == 'I']
        df_internacao = df_internacao.drop_duplicates(subset='FAT_NUM').reset_index(drop=True)
        df_internacao['FAT_NUM'] = df_internacao['FAT_NUM'].str.rstrip('.0').astype(int)
        
        st.dataframe(df_internacao)
    elif arquivo_atendimentos is None and arquivo_demonstrativo is not None:
        st.warning("Por favor, carregue o arquivo 'Atendimentos'.")



def page_tratamento():
    st.image("LOGO.png", width=150)
    st.header('Filtragem de dados sobre Tratamento')
    
    # Carregamento do arquivo 'Demonstrativo'
    arquivo_demonstrativo = st.file_uploader("Escolha o arquivo 'Demonstrativo' em formato xls")
    nomes_colunas_guias = ['Guia', 'Dt item']
    valores_guias = []

    if arquivo_demonstrativo is not None:
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

        # Aplicando os filtros
        df_filtrado = ler_e_filtrar_xls(arquivo_demonstrativo, nomes_colunas_guias, valores_guias if guia else None, intervalo_data if data else None)

        if df_filtrado is not None:
            if df_filtrado.empty:
                st.markdown("<h3 style='color: red;'>Resultados não encontrados</h3>", unsafe_allow_html=True)
            else:
                st.write('Tabela filtrada pelos valores selecionados:')
                df_filtrado['Guia'] = df_filtrado['Guia'].astype(str).str.replace('.', '')
                st.dataframe(df_filtrado[['Guia', 'Dt item']])
    else:
        st.warning("Por favor, carregue o arquivo 'Demonstrativo'.")

    # Carregamento do arquivo 'Atendimentos'
    arquivo_atendimentos = st.file_uploader("Escolha o arquivo 'Atendimentos' em formato xls")
    
     
    if arquivo_demonstrativo is not None and arquivo_atendimentos is not None:
        df_demonstrativo = pd.read_excel(arquivo_demonstrativo, engine='xlrd')
        df_demonstrativo = df_demonstrativo[nomes_colunas_guias]
        df_demonstrativo = df_demonstrativo.astype(str)
        df_demonstrativo = df_demonstrativo.rename(columns={'Guia':'GUIA_ATENDIMENTO', 'Dt item':'DATA_GUIAS'})
        # df_demonstrativo['DATA_GUIAS'] = pd.to_datetime(df_demonstrativo['DATA_GUIAS'], format='%d/%m/%Y').dt.strftime('%d/%m/%Y')
        
        df_atendimentos = pd.read_excel(arquivo_atendimentos)
        df_atendimentos = df_atendimentos.astype(str)
        
        if valores_guias:
            valores_guias = [guia.strip() for guia in valores_guias if guia.strip().isdigit()]
            df_atendimentos = df_atendimentos[df_atendimentos['GUIA_ATENDIMENTO'].isin(valores_guias)]
        df_atendimentos['CTH_DTHR_INI'] = pd.to_datetime(df_atendimentos['CTH_DTHR_INI'], format='%Y-%m-%d %H:%M:%S.%f').dt.strftime('%Y/%m/%d')
        df_atendimentos['CTH_DTHR_FIN'] = pd.to_datetime(df_atendimentos['CTH_DTHR_FIN'], format='%Y-%m-%d %H:%M:%S.%f').dt.strftime('%Y/%m/%d')
        
        merge_df = pd.merge(df_demonstrativo, df_atendimentos, on='GUIA_ATENDIMENTO')
        df_filtrado_periodo = merge_df[(merge_df['DATA_GUIAS'] >= merge_df['CTH_DTHR_INI']) & (merge_df['DATA_GUIAS'] <= merge_df['CTH_DTHR_FIN'])]
        df_filtrado_periodo = df_filtrado_periodo.reset_index(drop=True)
        
        df_tratamento = df_filtrado_periodo[df_filtrado_periodo['HSP_TRAT_INT'] == 'T']

        df_tratamento = df_tratamento[df_tratamento.FAT_NUM != 'nan'].reset_index()

        df_tratamento = df_tratamento.drop(df_tratamento.columns[[0]], axis = 1)

        df_tratamento['FAT_NUM'] = df_tratamento['FAT_NUM'].str.rstrip('.0')

        df_tratamento['FAT_NUM'] = pd.to_numeric(df_tratamento['FAT_NUM'])


        
        st.dataframe(df_tratamento)
    elif arquivo_atendimentos is None and arquivo_demonstrativo is not None:
        st.warning("Por favor, carregue o arquivo 'Atendimentos'.")




st.sidebar.title("Navegação")
page = st.sidebar.radio("", ["INTERNAÇÃO", "TRATAMENTO"])

if page == "INTERNAÇÃO":
    main_page()
else:
    page_tratamento()

