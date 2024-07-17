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
    # st.image exibe uma imagem na aplicação
    st.image("LOGO.png", width=150)
    # st.header é um método que exibe um cabeçalho na interface
    st.header('Filtragem de dados sobre Internação')

    # st.file_uploader é um método para fazer upload de arquivos
    uploaded_file = st.file_uploader("Escolha o arquivo 'Demonstrativo' em formato xls")

    # st.markdown('<p class="primary-color">Este é um exemplo de texto com a cor primária.</p>', unsafe_allow_html=True)

    # especificando o nome das colunas que trará para a filtragem inicial
    column_names = ['Guia', 'Dt item']
    # lista dos valores de guia que serão digitados 
    guide_values = []

    # se tiver selecionado o arquivo demonstrativo
    if uploaded_file is not None:
        # o checkbox para filtrar por guia
        guia = st.checkbox("Filtro Guia", value=False)
        # se o checkbox de guia for selecionado
        if guia:
            # atribuir a guide_values os valores de guias digitados
            guide_values = st.text_input('Digite os valores das guias separados por vírgulas').split(',')

        # o checkbox para filtrar por data
        data = st.checkbox("Filtro Data", value=True)
        date_range = None
        # se o checkbox de data for selecionado
        if data:
            # atribuir a guide_values os valores de datas
            date_range = st.date_input(
                "Selecione o intervalo de datas",
                value=(datetime(2024, 1, 1).date(), datetime(2024, 12, 31).date())
            )

        # antes tinha um botão de aplicar filtros
        # if st.button('Aplicar Filtros'):

            # passa para a função read_and_filter_xls, que usa esses parâmetros para filtrar os dados de acordo 
            # com os valores de guia(guide_values_to_use) e o intervalo de datas selecionados(date_range_to_use)
            guide_values_to_use = guide_values if guia else None
            date_range_to_use = date_range if data else None

            # está chamando a função de ler e filtrar a planilha, está lendo a planilha inserida,
            # pegando as colunas desejadas e filtrando de acordo com as guias e datas selecionadas
            df_filtered = read_and_filter_xls(uploaded_file, column_names, guide_values_to_use, date_range_to_use)
            if df_filtered is not None:
             
                # se o valor de guia não corresponder ou estiver vazio
                if df_filtered.empty:
                    st.markdown("<h3 style='color: red;'>Digite um valor de guia válido</h3>", unsafe_allow_html=True)
                else:
                    # caso contrário, filtrar por guia e data
                    st.write('Tabela filtrada pelos valores selecionados:')
                    st.dataframe(df_filtered[['Guia', 'Dt item']])
                    
                    # filtrar data item pegando a data mínima 
                    min_date = df_filtered['Dt item'].min()
                    min_date2 = pd.to_datetime(min_date, format= "%Y-%m-%d %H:%M:%S")
                    
                    st.write(f"A menor data encontrada é: {min_date2}")

                #     df_filtered_by_min_date = df_filtered[df_filtered['Dt item'] == min_date][['Guia', 'Dt item']]
                # # st.write('Tabela filtrada pela menor data:')
                # st.dataframe(df_filtered_by_min_date)
      
    else:
        st.write("Por favor, faça o upload de um arquivo XLS/XLSX.")

    st.header('Upload e Filtragem do Arquivo ATENDIMENTOS')

    uploaded_file2 = st.file_uploader("Escolha o arquivo 'Atendimentos' no formato xls", key="atendimentos")

    if uploaded_file2 is not None:
        df = pd.read_excel(uploaded_file2)
        df['Índice Original'] = df.index
        df_filtered_guia = df[
                df['GUIA_ATENDIMENTO'].isin(df.index) |
                df['GUIA_CONTA'].isin(df.index) |
                df['GIH_NUMERO'].isin(df.index)
            ]

        df['GUIA_ATENDIMENTO'] = df['GUIA_ATENDIMENTO'].astype(str).str.replace('.', '')
        df['GUIA_CONTA'] = df['GUIA_CONTA'].astype(str).str.replace('.', '')
        df['GIH_NUMERO'] = df['GIH_NUMERO'].astype(str).str.replace('.', '')

        if guide_values:
            df_filtered_guia = df['GUIA_ATENDIMENTO'].isin(guide_values) 

        else:
            df_filtered_guia = df.copy()

        if 'df_filtered' in locals() and not df_filtered.empty:
            
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
    # st.image exibe uma imagem na aplicação
    st.image("LOGO.png", width=150)
    # st.header é um método que exibe um cabeçalho na interface
    st.header('Filtragem de dados sobre Tratamento')

    # st.file_uploader é um método para fazer upload de arquivos
    uploaded_file = st.file_uploader("Escolha o arquivo 'Demonstrativo' em formato xls")

    # especificando o nome das colunas que trará para a filtragem inicial
    column_names = ['Guia', 'Dt item']
    # lista dos valores de guia que serão digitados 
    guide_values = []


    # se tiver selecionado o arquivo demonstrativo
    if uploaded_file is not None:
        
        # o checkbox para filtrar por guia
        guia = st.checkbox("Filtro Guia", value=False)
        # se o checkbox de guia for selecionado
        if guia:
            # atribuir a guide_values os valores de guias digitados
            guide_values = st.text_input('Digite os valores das guias separados por vírgulas').split(',')

        # o checkbox para filtrar por data
        data = st.checkbox("Filtro Data", value=True)
        date_range = None
        # se o checkbox de data for selecionado
        if data:
            # selecione o intervalo de data
            date_range = st.date_input(
                "Selecione o intervalo de datas",
                value=(pd.to_datetime('2024-01-01').date(), pd.to_datetime('2024-12-31').date())
            )

        # tinha um botão de aplicar filtros
        # if st.button('Aplicar Filtros'):
            

            # passa para a função read_and_filter_xls, que usa esses parâmetros para filtrar os dados de acordo 
            # com os valores de guia(guide_values_to_use) e o intervalo de datas selecionados(date_range_to_use)
            guide_values_to_use = guide_values if guia else None
            date_range_to_use = date_range if data else None

            # está chamando a função de ler e filtrar a planilha, está lendo a planilha inserida,
            # pegando as colunas desejadas e filtrando de acordo com as guias e datas selecionadas
            df_filtered = read_and_filter_xls(uploaded_file, column_names, guide_values_to_use, date_range_to_use)

            # se df_filtered não for vazio, aparecerá a tabela filtrada, com as guias e datas  
            if df_filtered is not None:
                st.write('Tabela filtrada pelos valores selecionados:')
                # st.dataframe exibe a tabela de forma interativa, com ordenação, com barra de rolagem, redimensionamento de colunas e pesquisa
                st.dataframe(df_filtered[['Guia', 'Dt item']])
                
                # min date pega a data mínima da coluna Dt item e exibe
                min_date = df_filtered['Dt item'].min()
                st.write(f"A menor data encontrada é: {min_date}")

                df_filtered_by_min_date = df_filtered[df_filtered['Dt item'] == min_date][['Guia', 'Dt item']]
                st.write('Tabela filtrada pela menor data:')
                st.dataframe(df_filtered_by_min_date)
        
        # exibe as informações do arquivo
        st.write(f'Nome do arquivo: {uploaded_file.name}')
        st.write(f'Tamanho do arquivo: {uploaded_file.size} bytes')
    # caso não tenha selecionado nenhum arquivo
    else:
        st.write("Por favor, faça o upload de um arquivo XLS/XLSX.")
    
    # st.header é um método que exibe um cabeçalho na interface
    st.header('Upload e Filtragem do Arquivo ATENDIMENTOS')

    # pede para inserir a segunda planilha, que será a de atendimentos
    uploaded_file2 = st.file_uploader("Escolha o arquivo 'Atendimentos' no formato xls", key="atendimentos")

    # caso seja inserido um arquivo 
    if uploaded_file2 is not None:
        # ler esse arquivo
        df = pd.read_excel(uploaded_file2)
        
        # Remover pontos dos valores nas colunas relevantes
        df['GUIA_ATENDIMENTO'] = df['GUIA_ATENDIMENTO'].apply(lambda x: str(x).replace('.', ''))
        df['GIH_NUMERO'] = df['GIH_NUMERO'].apply(lambda x: str(x).replace('.', ''))
        guide_values = [str(value).replace('.', '') for value in guide_values]

        # se filtrar por guias
        if guide_values:
            # vai verificar se os valores de guias filtrados correspondem a GUIA_atendimento
            df_filtered_guia = df[df['GUIA_ATENDIMENTO'].isin(guide_values)]
        # caso contrário, ria uma cópia completa do DataFrame df e a armazena na variável df_filtered_guia.
        # Assim podendo alterar o dataframe, sem alterar o original
        else:
            df_filtered_guia = df.copy()

        # locals() verifica se existem no escopo local as seguintes variáveis
        if 'guide_values_to_use' in locals() and 'df_filtered_guia' in locals() and 'df_filtered' in locals():

            # filtra para pegar apenas as linhas em que CTH_NUM for igual a 0
            df_filtered_guia = df_filtered_guia[df_filtered_guia['CTH_NUM'] == 0]
            # filtra para pegar apenas as linhas em que GUIA_ATENDIMENTO for igual GIH_NUMERO 
            df_filtered_guia = df_filtered_guia[df_filtered_guia['GUIA_ATENDIMENTO'] == df_filtered_guia['GIH_NUMERO']]
            # as guias que seram mostradas
            df_filtered2 = df_filtered_guia[['GUIA_ATENDIMENTO', 'GUIA_CONTA', 'HSP_NUM', 'HSP_PAC', 'CTH_NUM', 'FAT_SERIE', 'FAT_NUM', 'NFS_SERIE', 'NFS_NUMERO']]
            # transforma em string a seguinte coluna
            df_filtered2['NFS_NUMERO'] = df_filtered2['NFS_NUMERO'].astype(str)
            # renomeia os nomes das colunas
            df_filtered2 = df_filtered2.rename(columns={'HSP_NUM':'IH', 'HSP_PAC':'REGISTRO', 'CTH_NUM':'CONTA', 'FAT_SERIE':'PRE.S', 'FAT_NUM':'PRE.NUM', 'NFS_SERIE':'FAT.S', 'NFS_NUMERO':'FAT.NUM'})
            # junta as colunas guia e dt item da primeira planilha, com as colunas da segunda planilha
            result = pd.merge(df_filtered[['Guia', 'Dt item']], df_filtered2, left_on='Guia', right_on='GUIA_ATENDIMENTO', how='inner')
                
            # evitar valores duplicados de guias
            result.drop_duplicates(subset=['Guia'], keep='first', inplace=True)
            
            # exibe o resultado
            st.dataframe(result)

            # baixar o arquivo para o excel
            output2 = BytesIO()
            result.to_excel(output2, index=False)                   
            output2.seek(0)
            # botão de download
            st.download_button(
                label="Baixar arquivo Excel",
                data=output2,
                file_name=f"resultado_atendimentos_filtrado_{datetime.today().strftime('%Y-%m-%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            ) 
    # st.write é um método do streamlit que escreve algo na tela, tipo um print
    else:
        st.write("Por favor, faça o upload do arquivo ATENDIMENTOS v3.xls.")

# Navegação entre páginas
# o título do sidebar
st.sidebar.title("Navegação")
#  as opções de páginas exibidas no sidebar
page = st.sidebar.radio("", ["INTERNAÇÃO", "TRATAMENTO"])

# se clicar em internação, levará a página de internação, que é tudo que está dentro do main_page
if page == "INTERNAÇÃO":
    main_page()
# caso contrário, direciona para a página de tratamento, que é tudo que está dentro do page_tratamento 
else:
    page_tratamento()
