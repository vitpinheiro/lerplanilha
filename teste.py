
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

# Função responsável por gerenciar a página "Internação" da aplicação
def page_internacao():
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

        # Astype(str) - Transforma os dados de cada linha do dataframe em tipo string
        # Str.replace('.', '') - Método referente aos elementos do tipo 'string' que modifica
        # os elementos antes da vírgula pelos elementos depois da vírgula
        df['GUIA_ATENDIMENTO'] = df['GUIA_ATENDIMENTO'].astype(str).str.replace('.', '')
        df['GUIA_CONTA'] = df['GUIA_CONTA'].astype(str).str.replace('.', '')
        df['GIH_NUMERO'] = df['GIH_NUMERO'].astype(str).str.replace('.', '')

        # Verifica se a variável é verdadeira
        if guide_values:
            # Cria uma variável com os dados referentes à coluna "guia_atendimento" que pertencem ao conjunto de valores "guide_values"
            df_filtered_guia = df['GUIA_ATENDIMENTO'].isin(guide_values) 

        else:
            # Cria a mesma variável, mas copiando o dataframe antiga
            df_filtered_guia = df.copy()

        # Verifica se a variável "df_filtered" está contida nos elementos locais (contrário de elementos globais) e se é um dataframe não nulo
        if 'df_filtered'in locals() and not df_filtered.empty:

            # Atribui à variável o dataframe que obedecem às condições fornecidas
            df_filtered2 = df_filtered_guia[df_filtered_guia['GUIA_ATENDIMENTO'] == df_filtered_guia['GIH_NUMERO']]

            # Atribui à variável apenas os dados das colunas especificadas
            df_filtered2 = df_filtered2[['GUIA_ATENDIMENTO','GUIA_CONTA','HSP_NUM', 'HSP_PAC', 'CTH_NUM', 'FAT_SERIE', 'FAT_NUM', 'NFS_SERIE', 'NFS_NUMERO', 'CTH_DTHR_INI', 'CTH_DTHR_FIN']]
            
            # Torna os elementos das colunas especificadas em tipo "string"
            df_filtered2['NFS_NUMERO'] = df_filtered2['NFS_NUMERO'].astype(str)
            df_filtered2['HSP_PAC'] = df_filtered2['HSP_PAC'].astype(str)
            df_filtered2['FAT_NUM'] = df_filtered2['FAT_NUM'].astype(str)

            # Renomeia as colunas do dataframe para os nomes dispostos para depois dos ":"
            df_filtered2 = df_filtered2.rename(columns={'HSP_NUM':'IH', 'HSP_PAC':'REGISTRO', 'CTH_NUM':'CONTA', 'FAT_SERIE':'PRE.S', 'FAT_NUM':'PRE.NUM', 'NFS_SERIE':'FAT.S', 'NFS_NUMERO':'FAT.NUM', 'CTH_DTHR_INI':'DATA_INICIO', 'CTH_DTHR_FIN':'DATA_FIM'})
            
            # Merge para encontrar apenas as linhas em comum com 'GUIA_ATENDIMENTO'
            result = pd.merge(df_filtered[['Guia', 'Dt item']], df_filtered2, left_on='Guia', right_on='GUIA_ATENDIMENTO', how='inner')

            # Remove os elementos duplicados da variável            
            result.drop_duplicates(subset=['Guia'], keep='first', inplace=True)

            # Mostra na tela o dataframe resultado de todos os processos e filtragens
            st.dataframe(result)

            # Cria um "buffer de memória" que pode ser utilizado para leitura de dados de dados binários
            output2 = BytesIO()

            # Transforma o dataframe resultado em formato excel, desconsiderando os índices
            result.to_excel(output2, index=False)

            # Esse método movimenta o cursor para o início do buffer, garantindo que a leitura comece deste ponto
            output2.seek(0)

            # Cria um botão de download, responsável por baixar o arquivo "result" em formato excel
            st.download_button(
                label = "Baixar arquivo Excel",
                data = output2,
                file_name = f"resultado_atendimentos_filtrado_{datetime.today().strftime('%Y-%m-%d')}.xlsx",
                mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )      
    else:
        # Escreve na tela a mensagem especificada entre aspas 
        st.write("Por favor, faça o upload do arquivo 'Atendimentos'!")

# Função responsável por gerenciar a página "Tratamento" da aplicação
def page_tratamento():
    # Cria uma imagem com a logo fornecida, de tamanho 60px
    st.image("LOGO.png", width=60)

    # Cria um título para a seção
    st.header('Filtragem de dados sobre Tratamento')

    # Cria um input que recebe um arquivo em formato xls
    uploaded_file = st.file_uploader("Escolha o arquivo 'Demonstrativo' em formato xls")

    # Cria uma variável com os nomes das colunas de interesse 
    column_names = ['Guia', 'Dt item']

    # Cria uma variável vazia que receberá valores posteriormente
    guide_values = []

    # Verifica se algum arquivo foi inserido na variável "uploaded_file"
    if uploaded_file is not None:
        
        # Cria uma variável associada a um checkbox que recebe valor "False" se a checkbox estiver desmarcada e vice-versa
        guia = st.checkbox("Filtro Guia", value=False)

        # Verifica o estado da variável "guia"
        if guia:
            # Recupera o valor das guias inseridas em um text input e os separa por vírgulas em uma variável
            guide_values = st.text_input('Digite os valores das guias separados por vírgulas').split(',')

        # Cria uma variável associada a um checkbox que recebe valor "False" se a checkbox estiver desmarcada e vice-versa
        data = st.checkbox("Filtro Data", value=True)

        # Cria uma variável e associa a ela o valor "None"
        date_range = None

        # Verifica o estado da variável "data"
        if data:
            # Recupera o intervalo de data selecionado em um input em formato de calendário e o armazena em uma variável
            date_range = st.date_input(
                "Selecione o intervalo de datas",
                value=(pd.to_datetime('2024-01-01').date(), pd.to_datetime('2024-12-31').date())
            )

        # Associa à variável "guide_values_to_use" o valor de "guide_values" se o filtro de guia estiver ativo, caso contrário será vazio
        guide_values_to_use = guide_values if guia else None

        # Associa à variável "date_range_to_use" o valor de "date_range" se o filtro de data estiver ativo, caso contrário será vazio
        date_range_to_use = date_range if data else None

        # Modifica a variável "df_filtered" para receber o valor de uma planilha lida sob os parâmetros fornecidos
        df_filtered = read_and_filter_xls(uploaded_file, column_names, guide_values_to_use, date_range_to_use)

        # Condicional que verifica se a variável "df_filtered" é nula
        if df_filtered is not None:
            # Cria um elemento na tela que escreve o texto disposto entre aspas
            st.write('Tabela filtrada pelos valores selecionados:')

            # Elemento que exibe o dataframe na tela considerando as colunas especificadas
            st.dataframe(df_filtered[['Guia', 'Dt item']])
            
            # Cria uma variável que armazena o valor da menor data presente dentre os elementos da coluna específicada
            min_date = df_filtered['Dt item'].min()

            # Cria uma variável que representa um dataframe filtrado pela menor data fornecida acima 
            df_filtered_by_min_date = df_filtered[df_filtered['Dt item'] == min_date][['Guia', 'Dt item']]

            # Elemento que escreve na tela o texto especificado entre aspas
            st.write('Tabela filtrada pela menor data:')

            # # Elemento que exibe o dataframe na tela
            st.dataframe(df_filtered_by_min_date)

        # Elemento que escreve na tela o texto especificado entre aspas
        st.write(f'Nome do arquivo: {uploaded_file.name}')

        # Elemento que escreve na tela o texto especificado entre aspas
        st.write(f'Tamanho do arquivo: {uploaded_file.size} bytes')
    else:
        # Elemento que escreve na tela o texto especificado entre aspas
        st.write("Por favor, faça o upload de um arquivo XLS/XLSX.")

    # Cria um título para a seção
    st.header('Upload e Filtragem do Arquivo ATENDIMENTOS')

    # Atribui à variável o arquivo lido
    uploaded_file2 = st.file_uploader("Escolha o arquivo 'Atendimentos' no formato xls", key="atendimentos")

    # Verifica se a variável não é nula
    if uploaded_file2 is not None:

        # Cria um dataframe a partir da leitura do arquivo excel
        df = pd.read_excel(uploaded_file2)
        
        # Remover pontos dos valores nas colunas relevantes, substituindo-os por espaços vazios
        df['GUIA_ATENDIMENTO'] = df['GUIA_ATENDIMENTO'].apply(lambda x: str(x).replace('.', ''))
        df['GIH_NUMERO'] = df['GIH_NUMERO'].apply(lambda x: str(x).replace('.', ''))
        guide_values = [str(value).replace('.', '') for value in guide_values]

        # Verifica se a variável é verdadeira
        if guide_values:
            # Realiza uma filtragem no dataframe
            df_filtered_guia = df[df['GUIA_ATENDIMENTO'].isin(guide_values) | df['GIH_NUMERO'].isin(guide_values)]
        else:
            # Atribui à variável uma cópia do dataframe original
            df_filtered_guia = df.copy()

        # Verifica se os valores listados encontram-se entre os elementos locais
        if 'guide_values_to_use' in locals() and 'df_filtered_guia' in locals() and 'df_filtered' in locals():

            # realiza uma filtragem retornando as linhas em que os elementos da coluna "CTH_NUM" são iguais a 0
            df_filtered_guia = df_filtered_guia[df_filtered_guia['CTH_NUM'] == 0]

            # Realiza uma filtragem retornando as linhas em que os elementos da coluna "GUIA_ATENDIMENTO" são iguais aos da coluna "GIH_NUMERO"
            df_filtered_guia = df_filtered_guia[df_filtered_guia['GUIA_ATENDIMENTO'] == df_filtered_guia['GIH_NUMERO']]

            # Cria um dataframe com os elementos referentes apenas às colunas especificadas
            df_filtered2 = df_filtered_guia[['GUIA_ATENDIMENTO', 'GUIA_CONTA', 'HSP_NUM', 'HSP_PAC', 'CTH_NUM', 'FAT_SERIE', 'FAT_NUM', 'NFS_SERIE', 'NFS_NUMERO']]
            
            # Torna os valores referentes à coluna selecionada em tipo "string"
            df_filtered2['NFS_NUMERO'] = df_filtered2['NFS_NUMERO'].astype(str)

            # Modifica o nome das colunas do dataframe para o nome disposto depois dos ":"
            df_filtered2 = df_filtered2.rename(columns={'HSP_NUM':'IH', 'HSP_PAC':'REGISTRO', 'CTH_NUM':'CONTA', 'FAT_SERIE':'PRE.S', 'FAT_NUM':'PRE.NUM', 'NFS_SERIE':'FAT.S', 'NFS_NUMERO':'FAT.NUM'})
            
            # Merge para encontrar apenas as linhas em comum com 'GUIA_ATENDIMENTO'
            result = pd.merge(df_filtered[['Guia', 'Dt item']], df_filtered2, left_on='Guia', right_on='GUIA_ATENDIMENTO', how='inner')
                
            # Remove os elementos duplicados 
            result.drop_duplicates(subset=['Guia'], keep='first', inplace=True)

            # Exibe o dataframe na tela
            st.dataframe(result)
        
            # Cria um "buffer de memória" que pode ser utilizado para leitura de dados de dados binários
            output2 = BytesIO()

            # Transforma o dataframe resultado em formato excel, desconsiderando os índices
            result.to_excel(output2, index=False)

            # Esse método movimenta o cursor para o início do buffer, garantindo que a leitura comece deste ponto
            output2.seek(0)

            # Cria um botão de download, responsável por baixar o arquivo "result" em formato excel
            st.download_button(
                label="Baixar arquivo Excel",
                data=output2,
                file_name=f"resultado_atendimentos_filtrado_{datetime.today().strftime('%Y-%m-%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            ) 
        else:
            # Exibe uma mensagem na tela
            st.markdown(
            "<h3 style='color: red; font-weight: bold;'>Por favor, primeiro clique em aplicar filtro</h3>",
            unsafe_allow_html=True
            )
    else:
        # Exibe uma mensagem na tela
        st.write("Por favor, faça o upload do arquivo ATENDIMENTOS v3.xls.")

# Elemento que escreve o título da barra de navegação
st.sidebar.title("Navegação")

# Define as páginas possíveis para navegação
page = st.sidebar.radio("", ["INTERNAÇÃO", "TRATAMENTO"])

# Condicional que define qual página estará ativa
if page == "INTERNAÇÃO":
    page_internacao()
else:
    page_tratamento()