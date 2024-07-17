
# Importação das bibliotecas responsáveis, respectivamente, por: tratamento de dados, 
# criação e manutenção interface gráfica, tratamento de memória e gestão de arquivos e 
# tratamento de valores de data

import pandas as pd
import streamlit as st
from io import BytesIO
from datetime import datetime


# Função responsável pela leitura dos arquivos em formato ".xls". Recebe como 
# parâmetros o arquivo, o nome das colunas, o valor das guias e o intervalo de datas

def read_and_filter_xls(file, column_names, guide_values, date_range):

    # Criação do dataframe (espécie de tabela) a partir do arquivo fornecido
    df = pd.read_excel(file)

    # Verifica se a coluna "Guia" encontra-se entre o nome das colunas do dataframe e houver valores de guia
    if 'Guia' in column_names and guide_values:
        # Atualiza o dataframe para que contenha apenas os valores de guia 
        df = df[df['Guia'].astype(str).isin(guide_values)]

    # Verifica se a coluna "Dt item" encontra-se entre o nome das colunas do dataframe e houver valores de data  
    if 'Dt item' in column_names and date_range:
        # Converte os valores da coluna Dt item para formato datetime
        df['Dt item'] = pd.to_datetime(df['Dt item'], dayfirst=True, errors='coerce')
        # Atualiza o dataframe para que contenha apenas os valores de data
        df = df[(df['Dt item'] >= pd.to_datetime(date_range[0])) & (df['Dt item'] <= pd.to_datetime(date_range[1]))]
    
    # Retorna o dataframe modificado
    return df

# Função responsável por gerenciar a página principal da aplicação
def main_page():
    # Cria uma imagem com a logo fornecida, de tamanho 60px
    st.image("LOGO.png", width=60)

    # Cria um título para a seção
    st.header('Filtragem de dados sobre Internação')

    # Cria um input que recebe um arquivo em formato xls
    uploaded_file = st.file_uploader("Escolha o arquivo 'Demonstrativo' em formato xls")

    # Cria uma variável com os nomes das colunas de interesse 
    column_names = ['Guia', 'Dt item']

    # Cria uma variável vazia que receberá valores posteriormente
    guide_values = []

    # Verifica se algum arquivo foi inserido na variável "uploaded_file"
    if uploaded_file is not None:

        # Cria uma variável associada a um checkbox que recebe valor "False" se a checkbox estiver desmarcada e vice-versa
        guia = st.checkbox("Filtro Guia", value = False)

        # Verifica o estado da variável "guia"
        if guia:
            # Recupera o valor das guias inseridas em um text input e os separa por vírgulas em uma variável
            guide_values = st.text_input('Digite os valores das guias separados por vírgulas').split(',')

        # Cria uma variável associada a um checkbox que recebe valor "False" se a checkbox estiver desmarcada e vice-versa
        data = st.checkbox("Filtro Data", value = True)

        # Cria uma variável e associa a ela o valor "None"
        date_range = None

        # Verifica o estado da variável "data"
        if data:
            # Recupera o intervalo de data selecionado em um input em formato de calendário e o armazena em uma variável
            date_range = st.date_input(
                "Selecione o intervalo de datas",
                value=(datetime(2024, 1, 1).date(), datetime(2024, 12, 31).date())
            )


        # Associa à variável "guide_values_to_use" o valor de "guide_values" se o filtro de guia estiver ativo, caso contrário será vazio
        guide_values_to_use = guide_values if guia else None

        # Associa à variável "date_range_to_use" o valor de "date_range" se o filtro de data estiver ativo, caso contrário será vazio
        date_range_to_use = date_range if data else None

        # Modifica a variável "df_filtered" para receber o valor de uma planilha lida sob os parâmetros fornecidos
        df_filtered = read_and_filter_xls(uploaded_file, column_names, guide_values_to_use, date_range_to_use)

        # Condicional que verifica se a variável "df_filtered" é nula
        if df_filtered is not None:
            
            # Verifica se a variável está vazia
            if df_filtered.empty:
                # Caso a variável esteja vazia, cria um elemento escrito na tela com as condições fornecidas
                st.markdown("<h3 style='color: red;'>Digite um valor de guia válido</h3>", unsafe_allow_html=True)
            else:
                # Cria um elemento escrito na tela precedente ao display da tabela
                st.write('Tabela filtrada pelos valores selecionados:')
                # Cria graficamente a tabela cujas colunas são fonecidas entre os colchetes
                st.dataframe(df_filtered[['Guia', 'Dt item']])
            
                # Resgata a menor data dentre os valores passados pelas filtragens
                min_date = df_filtered['Dt item'].min()

                # Converte o valor da variável "min_date" para datetime na formatação fornecida
                min_date = pd.to_datetime(min_date, format= "%Y-%m-%d")
                
                # Cria um elemento escrito na tela que fornece o valor da variável "min_date"
                st.write(f"A menor data encontrada é: {min_date}")
      
    else:
        # Caso as condicionais não sejam atendidas, cria um elemento na tela que escreve o texto entre parênteses
        st.write("Por favor, faça o upload de um arquivo XLS/XLSX.")

    # Cria um elemento de título com o texto entre as aspas
    st.header('Upload e Filtragem do Arquivo ATENDIMENTOS')

    # Cria um input que recebe um arquivo em formato xls
    uploaded_file2 = st.file_uploader("Escolha o arquivo 'Atendimentos' no formato xls", key="atendimentos")

    # Verifica se a variável "uploaded_file2" é vazia
    if uploaded_file2 is not None:

        # Cria um dataframe a partir da leitura do arquivo recuperado pela variável "uploaded_file2"
        df = pd.read_excel(uploaded_file2)

        
        df['GUIA_ATENDIMENTO'] = df['GUIA_ATENDIMENTO'].astype(str).str.replace('.', '')
        df['GUIA_CONTA'] = df['GUIA_CONTA'].astype(str).str.replace('.', '')
        df['GIH_NUMERO'] = df['GIH_NUMERO'].astype(str).str.replace('.', '')

        if guide_values:
            df_filtered_guia =df['GUIA_ATENDIMENTO'].isin(guide_values) 

        else:
            df_filtered_guia = df.copy()

        if 'df_filtered'in locals() and not df_filtered.empty:
            
            min_date = df_filtered['Dt item'].min()
            min_date2 = pd.to_datetime(min_date, format="%Y-%m-%d %H:%M:%S")
        

            df_filtered_guia['CTH_DTHR_INI'] = pd.to_datetime(df_filtered_guia['CTH_DTHR_INI'], errors='coerce')
            df_filtered_guia['CTH_DTHR_FIN'] = pd.to_datetime(df_filtered_guia['CTH_DTHR_FIN'], errors='coerce')

            # st.write(df_filtered_guia['CTH_DTHR_INI'])
            # st.write(df_filtered_guia['CTH_DTHR_FIN'])


            if len(df_filtered_guia) == 1:
                df_filtered2 = df_filtered_guia
            else:   
                df_filtered_guia = df_filtered_guia.loc[
                    (df_filtered_guia['CTH_DTHR_INI'] <= min_date2) &
                    (min_date2 <= df_filtered_guia['CTH_DTHR_FIN'])
                ]

            
            df_filtered2 = df_filtered_guia[df_filtered_guia['GUIA_ATENDIMENTO'] == df_filtered_guia['GIH_NUMERO']]
            df_filtered2 = df_filtered2[['GUIA_ATENDIMENTO','GUIA_CONTA','HSP_NUM', 'HSP_PAC', 'CTH_NUM', 'FAT_SERIE', 'FAT_NUM', 'NFS_SERIE', 'NFS_NUMERO', 'CTH_DTHR_INI', 'CTH_DTHR_FIN']]
            df_filtered2['NFS_NUMERO'] = df_filtered2['NFS_NUMERO'].astype(str)
            df_filtered2['HSP_PAC'] = df_filtered2['HSP_PAC'].astype(str)
            df_filtered2['FAT_NUM'] = df_filtered2['FAT_NUM'].astype(str)
            df_filtered2 = df_filtered2.rename(columns={'HSP_NUM':'IH', 'HSP_PAC':'REGISTRO', 'CTH_NUM':'CONTA', 'FAT_SERIE':'PRE.S', 'FAT_NUM':'PRE.NUM', 'NFS_SERIE':'FAT.S', 'NFS_NUMERO':'FAT.NUM', 'CTH_DTHR_INI':'DATA_INICIO', 'CTH_DTHR_FIN':'DATA_FIM'})
       
            # st.dataframe(df_filtered2)
            
            # Merge para encontrar apenas as linhas em comum com 'GUIA_ATENDIMENTO'
            result = pd.merge(df_filtered[['Guia', 'Dt item']], df_filtered2, left_on='Guia', right_on='GUIA_ATENDIMENTO', how='inner')
            
            
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
        # else:
        #     st.markdown(
        #     "<h3 style='color: red; font-weight: bold;'>Por favor, primeiro clique em aplicar filtro</h3>",
        #     unsafe_allow_html=True
        #     )
            
    else:
        st.write("Por favor, faça o upload do arquivo 'Atendimentos'!")

def page_tratamento():
    st.image("LOGO.png", width=150)
    st.header('Filtragem de dados sobre Tratamento')

    uploaded_file = st.file_uploader("Escolha o arquivo 'Demonstrativo' em formato xls")

    column_names = ['Guia', 'Dt item']
    guide_values = []

    if uploaded_file is not None:
        
        guia = st.checkbox("Filtro Guia", value=False)
        if guia:
            guide_values = st.text_input('Digite os valores das guias separados por vírgulas').split(',')

        data = st.checkbox("Filtro Data", value=True)
        date_range = None
        if data:
            date_range = st.date_input(
                "Selecione o intervalo de datas",
                value=(pd.to_datetime('2024-01-01').date(), pd.to_datetime('2024-12-31').date())
            )

        # if st.button('Aplicar Filtros'):
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

        st.write(f'Nome do arquivo: {uploaded_file.name}')
        st.write(f'Tamanho do arquivo: {uploaded_file.size} bytes')
    else:
        st.write("Por favor, faça o upload de um arquivo XLS/XLSX.")

    st.header('Upload e Filtragem do Arquivo ATENDIMENTOS')
    uploaded_file2 = st.file_uploader("Escolha o arquivo 'Atendimentos' no formato xls", key="atendimentos")

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

        if 'guide_values_to_use' in locals() and 'df_filtered_guia' in locals() and 'df_filtered' in locals():

        

            df_filtered_guia = df_filtered_guia[df_filtered_guia['CTH_NUM'] == 0]
            df_filtered_guia = df_filtered_guia[df_filtered_guia['GUIA_ATENDIMENTO'] == df_filtered_guia['GIH_NUMERO']]
            df_filtered2 = df_filtered_guia[['GUIA_ATENDIMENTO', 'GUIA_CONTA', 'HSP_NUM', 'HSP_PAC', 'CTH_NUM', 'FAT_SERIE', 'FAT_NUM', 'NFS_SERIE', 'NFS_NUMERO']]
            df_filtered2['NFS_NUMERO'] = df_filtered2['NFS_NUMERO'].astype(str)
            df_filtered2 = df_filtered2.rename(columns={'HSP_NUM':'IH', 'HSP_PAC':'REGISTRO', 'CTH_NUM':'CONTA', 'FAT_SERIE':'PRE.S', 'FAT_NUM':'PRE.NUM', 'NFS_SERIE':'FAT.S', 'NFS_NUMERO':'FAT.NUM'})
            result = pd.merge(df_filtered[['Guia', 'Dt item']], df_filtered2, left_on='Guia', right_on='GUIA_ATENDIMENTO', how='inner')
                
                
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