# junção de main.py e teste.py, aqui está a leitura e filtragem de demonstrativo primeiro(planilha fixa), logo após a leitura da planilha ATENDIMENTOS(terá conexão com o banco), onde compara se a guia filtrada inicilamente, será incluida na filtragem da outra, para ver se elas são iguais, mostrando uma outra tabela. Ambas podem ser baixadas para csv e xlsx
# fiz a conexao com um banco(teste apenas), no conexaobanco.py, estou importando aqui as funcoes de conexao

import pandas as pd
import streamlit as st
from io import BytesIO
from datetime import datetime
from conexaobanco import connect_to_database
from conexaobanco import execute_sql_query

# query = f"SELECT guia FROM guia"
# guia_from_database = execute_sql_query(query)


# Função para ler e filtrar o arquivo XLS
def read_and_filter_xls(xls_file, column_names, col_guia=None, date_range=None):
    try:
        # Ler o arquivo XLS e criar DataFrame
        df = pd.read_excel(xls_file)

        # Filtrar apenas as colunas especificadas
        df_filtered = df[column_names]

       
        if col_guia:
            df_filtered = df_filtered[df_filtered['Guia'].astype(str).str.contains(col_guia)]

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

# Interface do Streamlit
st.image("LOGO.png", width=150)
st.title('Leitura e Filtro de Arquivo XLS')

# Upload de arquivo
uploaded_file = st.file_uploader("Escolha um arquivo XLS/XLSX")

column_names = ['Guia', 'Dt item']
col_guia = None


if uploaded_file is not None:
    
    guia = st.checkbox("Filtro Guia", value=True)
    if guia:
        col_guia = st.text_input('Digite o valor para a coluna "Guia"')

   
    data = st.checkbox("Filtro Data", value=True)
    if data:
        date_range = st.date_input(
            "Selecione o intervalo de datas para a coluna 'Dt item'",
            value=(pd.to_datetime('2024-01-01').date(), pd.to_datetime('2024-12-31').date())
        )

 
    if st.button('Aplicar Filtros'):
        df_filtered = read_and_filter_xls(uploaded_file, column_names, col_guia if guia else None, date_range if data else None)
        
        if df_filtered is not None:
            st.write('Tabela filtrada pelos valores selecionados:')
            st.dataframe(df_filtered)
            
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


    st.write(f'Nome do arquivo: {uploaded_file.name}')
    st.write(f'Tamanho do arquivo: {uploaded_file.size} bytes')
else:
    st.write("Por favor, faça o upload de um arquivo XLS/XLSX.")

# Carregar a planilha ATENDIMENTOS.xls
uploaded_file2 = st.file_uploader("Escolha o arquivo ATENDIMENTOS.xls", key="atendimentos")

if uploaded_file2 is not None:
    if col_guia is not None:
 
        df = pd.read_excel(uploaded_file2)

    
        colunas_guia = [col_guia, 'GUIA_ATENDIMENTO', 'GUIA_CONTA', 'GIH_NUMERO']

      
        df_filtered_guia = df[df.isin(colunas_guia).any(axis=1)]

    
        df_filtered_guia = df_filtered_guia[df_filtered_guia['CTH_NUM'] == 1]
        df_filtered_guia = df_filtered_guia[df_filtered_guia['GUIA_CONTA'] == df_filtered_guia['GIH_NUMERO']]


        df_filtered2 = df_filtered_guia[['HSP_NUM', 'HSP_PAC', 'CTH_NUM', 'FAT_SERIE', 'FAT_NUM', 'GUIA_ATENDIMENTO', 'GUIA_CONTA', 'GIH_NUMERO']]

  
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
    st.write("Por favor, faça o upload do arquivo ATENDIMENTOS.xls.")
