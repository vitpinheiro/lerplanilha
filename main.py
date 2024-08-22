# Importação das bibliotecas responsáveis, respectivamente, por: tratamento de dados, 
# criação e manutenção interface gráfica, tratamento de memória e gestão de arquivos e 
# tratamento de valores de data

import pandas as pd
import streamlit as st
from io import BytesIO
from datetime import datetime, timedelta

hoje = datetime.now()

data_ano_anterior = hoje - timedelta(days = 365)

# Função responsável pela leitura dos arquivos em formato ".xls". Recebe como 
# parâmetros o arquivo, o nome das colunas, o valor das guias e o intervalo de datas

def ler_planilha(file, nomes_colunas_guias, intervalo_data):

    # Criação do dataframe (espécie de tabela) a partir do arquivo fornecido
    df = pd.read_excel(file, engine='xlrd')

    # Criar um objeto BytesIO para armazenar o arquivo .xlsx em memória
    output = BytesIO()

    # Salvar o DataFrame como um arquivo .xlsx no objeto BytesIO
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    
    # Mover o ponteiro do objeto BytesIO para o início
    output.seek(0)

    # Modifica a variável df para que seja um arquivo .xlsx
    df = pd.read_excel(output)

    # Reinicia os índices do dataframe
    df.reset_index(drop=True, inplace=True)

    # # Verifica se a coluna "Guia" encontra-se entre o nome das colunas do dataframe e houver valores de guia
    # if 'Guia' in nomes_colunas_guias and valores_de_guias:
    #     # Atualiza o dataframe para que contenha apenas os valores de guia 
    #     df = df[df['Guia'].astype(str).isin(valores_de_guias)]

    # Verifica se a coluna "Dt item" encontra-se entre o nome das colunas do dataframe e houver valores de data  
    if 'Dt item' in nomes_colunas_guias and intervalo_data:
        # Converte os valores da coluna Dt item para formato datetime
        df['Dt item'] = pd.to_datetime(df['Dt item'], dayfirst=True, errors='coerce')
        # Atualiza o dataframe para que contenha apenas os valores de data
        df = df[(df['Dt item'] >= pd.to_datetime(intervalo_data[0])) & (df['Dt item'] <= pd.to_datetime(intervalo_data[1]))]
    
    # Retorna o dataframe modificado
    return df

# Função responsável por gerenciar a página "Internação" da aplicação
def page_internacao():
    # Cria uma imagem com a logo fornecida, de tamanho 60px
    st.image("LOGO.png", width=60)

    # Cria um título para a seção
    st.header('Filtragem de dados sobre Internação')

    # Cria um input que recebe um arquivo em formato xls
    arquivo_demonstrativo = st.file_uploader("Escolha o arquivo 'Demonstrativo' em formato xls")

    # Cria uma variável com os nomes das colunas de interesse 
    nomes_colunas_guias = ['Guia', 'Dt item']

    valores_de_guias = []

    # Verifica se algum arquivo foi inserido na variável "uploaded_file"
    if arquivo_demonstrativo is not None:

        # # Cria uma variável associada a um checkbox que recebe valor "False" se a checkbox estiver desmarcada e vice-versa
        # check_guia = st.checkbox("Filtro Guia", value = False)

        # # Verifica o estado da variável "guia"
        # if check_guia:
        #     # Recupera o valor das guias inseridas em um text input e os separa por vírgulas em uma variável
        #     valores_de_guias = st.text_input('Digite os valores das guias separados por vírgulas').split(',')

        # Cria uma variável associada a um checkbox que recebe valor "False" se a checkbox estiver desmarcada e vice-versa
        check_data = st.checkbox("Filtro Data", value = True)

        # Cria uma variável e associa a ela o valor "None"
        intervalo_data = None

        # Verifica o estado da variável "data"
        if check_data:
            # Recupera o intervalo de data selecionado em um input em formato de calendário e o armazena em uma variável
            intervalo_data = st.date_input(
                "Selecione o intervalo de datas",
                value=(data_ano_anterior.date(), hoje.date())
            )

        # Associa à variável "valores_de_guias_uteis" o valor de "valores_de_guias" se o filtro de guia estiver ativo, caso contrário será vazio
        # valores_de_guias_uteis = valores_de_guias if check_guia else None



        # Associa à variável "intervalo_data_uteis" o valor de "intervalo_data" se o filtro de data estiver ativo, caso contrário será vazio
        intervalo_data_uteis = intervalo_data if check_data else None

        # Modifica a variável "df_filtered" para receber o valor de uma planilha lida sob os parâmetros fornecidos
        df_demonstrativo = ler_planilha(arquivo_demonstrativo, nomes_colunas_guias, intervalo_data_uteis)

        df_demonstrativo = df_demonstrativo[nomes_colunas_guias]

        df_demonstrativo = df_demonstrativo.astype(str)

        df_demonstrativo = df_demonstrativo.rename(columns={'Guia':'GUIA_ATENDIMENTO', 'Dt item':'DATA_GUIAS'})

        # Condicional que verifica se a variável "df_demonstrativo" é nula
        if df_demonstrativo is not None:
            # Verifica se a variável está vazia
            if df_demonstrativo.empty:
                # Caso a variável esteja vazia, cria um elemento escrito na tela com as condições fornecidas
                st.markdown("<h3 style='color: red;'>Digite um valor de guia válido</h3>", unsafe_allow_html=True)
            else:
                # Cria um elemento escrito na tela precedente ao display da tabela
                st.write('Tabela filtrada pelos valores selecionados:')
                # Cria graficamente a tabela cujas colunas são fonecidas entre os colchetes
                st.dataframe(df_demonstrativo)
      
    else:
        # Caso as condicionais não sejam atendidas, cria um elemento na tela que escreve o texto entre parênteses
        st.write("Por favor, faça o upload de um arquivo XLS/XLSX.")

    # Cria um elemento de título com o texto entre as aspas
    st.header('Upload e Filtragem do Arquivo ATENDIMENTOS')

    # Cria um input que recebe um arquivo em formato xls
    arquivo_atendimentos = st.file_uploader("Escolha o arquivo 'Atendimentos' no formato xls", key="atendimentos")

    # Verifica se a variável "arquivo_atendimentos" é vazia
    if arquivo_atendimentos is not None:

        # Cria um dataframe a partir da leitura do arquivo recuperado pela variável "arquivo_atendimentos"
        df_atendimentos = pd.read_excel(arquivo_atendimentos)

        df_atendimentos = df_atendimentos.astype(str)

        if valores_de_guias:
            valores_de_guias = [guia.strip() for guia in valores_de_guias if guia.strip().isdigit()]
            df_atendimentos = df_atendimentos[df_atendimentos['GUIA_ATENDIMENTO'].isin(valores_de_guias)]

        df_atendimentos['CTH_DTHR_INI'] = pd.to_datetime(df_atendimentos['CTH_DTHR_INI'], format='%Y-%m-%d %H:%M:%S.%f').dt.strftime('%Y-%m-%d')

        df_atendimentos['CTH_DTHR_FIN'] = pd.to_datetime(df_atendimentos['CTH_DTHR_FIN'], format='%Y-%m-%d %H:%M:%S.%f').dt.strftime('%Y-%m-%d')

        # Verifica se a variável "df_filtered" está contida nos elementos locais (contrário de elementos globais) e se é um dataframe não nulo
        if 'df_atendimentos' in locals() and not df_atendimentos.empty:

            merge_df = pd.merge(df_demonstrativo, df_atendimentos, on='GUIA_ATENDIMENTO')

            df_filtrado_periodo = merge_df[(merge_df['DATA_GUIAS'] >= merge_df['CTH_DTHR_INI']) & (merge_df['DATA_GUIAS'] <= merge_df['CTH_DTHR_FIN'])]

            df_internacao = df_filtrado_periodo[df_filtrado_periodo['HSP_TRAT_INT'] == 'I']

            df_internacao = df_internacao.drop_duplicates(subset='FAT_NUM').reset_index()

            df_internacao = df_internacao.drop(df_internacao.columns[[0]], axis = 1)

            df_internacao['FAT_NUM'] = df_internacao['FAT_NUM'].str.rstrip('.0')

            df_internacao['FAT_NUM'] = pd.to_numeric(df_internacao['FAT_NUM'])

            # Mostra na tela o dataframe resultado de todos os processos e filtragens
            st.dataframe(df_internacao)

            # Cria um "buffer de memória" que pode ser utilizado para leitura de dados de dados binários
            output2 = BytesIO()

            # Transforma o dataframe resultado em formato excel, desconsiderando os índices
            df_internacao.to_excel(output2, index=False)

            # Esse método movimenta o cursor para o início do buffer, garantindo que a leitura comece deste ponto
            output2.seek(0)

            # Cria um botão de download, responsável por baixar o arquivo "result" em formato excel
            st.download_button(
                label = "Baixar Internação.xls",
                data = output2,
                file_name = f"resultado_atendimentos_filtrado_{datetime.today().strftime('%Y-%m-%d')}.xls",
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
    st.header('Filtragem de dados sobre Tratamentos')

    # Cria um input que recebe um arquivo em formato xls
    arquivo_demonstrativo = st.file_uploader("Escolha o arquivo 'Demonstrativo' em formato xls")

    # Cria uma variável com os nomes das colunas de interesse 
    nomes_colunas_guias = ['Guia', 'Dt item']

    valores_de_guias = []

    # Verifica se algum arquivo foi inserido na variável "uploaded_file"
    if arquivo_demonstrativo is not None:

        # # Cria uma variável associada a um checkbox que recebe valor "False" se a checkbox estiver desmarcada e vice-versa
        # check_guia = st.checkbox("Filtro Guia", value = False)

        # # Verifica o estado da variável "guia"
        # if check_guia:
        #     # Recupera o valor das guias inseridas em um text input e os separa por vírgulas em uma variável
        #     valores_de_guias = st.text_input('Digite os valores das guias separados por vírgulas').split(',')

        # Cria uma variável associada a um checkbox que recebe valor "False" se a checkbox estiver desmarcada e vice-versa
        check_data = st.checkbox("Filtro Data", value = True)

        # Cria uma variável e associa a ela o valor "None"
        intervalo_data = None

        # Verifica o estado da variável "data"
        if check_data:
            # Recupera o intervalo de data selecionado em um input em formato de calendário e o armazena em uma variável
            intervalo_data = st.date_input(
                "Selecione o intervalo de datas",
                value=(data_ano_anterior.date(), hoje.date())
            )

        # # Associa à variável "valores_de_guias_uteis" o valor de "valores_de_guias" se o filtro de guia estiver ativo, caso contrário será vazio
        # valores_de_guias_uteis = valores_de_guias if check_guia else None

        # Associa à variável "intervalo_data_uteis" o valor de "intervalo_data" se o filtro de data estiver ativo, caso contrário será vazio
        intervalo_data_uteis = intervalo_data if check_data else None

        # Modifica a variável "df_filtered" para receber o valor de uma planilha lida sob os parâmetros fornecidos
        df_demonstrativo = ler_planilha(arquivo_demonstrativo, nomes_colunas_guias, intervalo_data_uteis)

        df_demonstrativo = df_demonstrativo[nomes_colunas_guias]

        df_demonstrativo = df_demonstrativo.astype(str)

        df_demonstrativo = df_demonstrativo.rename(columns={'Guia':'GUIA_ATENDIMENTO', 'Dt item':'DATA_GUIAS'})

        # Condicional que verifica se a variável "df_demonstrativo" é nula
        if df_demonstrativo is not None:
            # Verifica se a variável está vazia
            if df_demonstrativo.empty:
                # Caso a variável esteja vazia, cria um elemento escrito na tela com as condições fornecidas
                st.markdown("<h3 style='color: red;'>Digite um valor de guia válido</h3>", unsafe_allow_html=True)
            else:
                # Cria um elemento escrito na tela precedente ao display da tabela
                st.write('Tabela filtrada pelos valores selecionados:')
                # Cria graficamente a tabela cujas colunas são fonecidas entre os colchetes
                st.dataframe(df_demonstrativo)
      
    else:
        # Caso as condicionais não sejam atendidas, cria um elemento na tela que escreve o texto entre parênteses
        st.write("Por favor, faça o upload de um arquivo XLS/XLSX.")

    # Cria um elemento de título com o texto entre as aspas
    st.header('Upload e Filtragem do Arquivo ATENDIMENTOS')

    # Cria um input que recebe um arquivo em formato xls
    arquivo_atendimentos = st.file_uploader("Escolha o arquivo 'Atendimentos' no formato xls", key="atendimentos")

    # Verifica se a variável "arquivo_atendimentos" é vazia
    if arquivo_atendimentos is not None:

        # Cria um dataframe a partir da leitura do arquivo recuperado pela variável "arquivo_atendimentos"
        df_atendimentos = pd.read_excel(arquivo_atendimentos)

        df_atendimentos = df_atendimentos.astype(str)

        if valores_de_guias:
            valores_de_guias = [guia.strip() for guia in valores_de_guias if guia.strip().isdigit()]
            df_atendimentos = df_atendimentos[df_atendimentos['GUIA_ATENDIMENTO'].isin(valores_de_guias)]

        df_atendimentos['CTH_DTHR_INI'] = pd.to_datetime(df_atendimentos['CTH_DTHR_INI'], format='%Y-%m-%d %H:%M:%S.%f').dt.strftime('%Y-%m-%d')

        df_atendimentos['CTH_DTHR_FIN'] = pd.to_datetime(df_atendimentos['CTH_DTHR_FIN'], format='%Y-%m-%d %H:%M:%S.%f').dt.strftime('%Y-%m-%d')

        # Verifica se a variável é verdadeira
        if valores_de_guias:
            # Cria uma variável com os dados referentes à coluna "GUIA_ATENDIMENTO" que pertencem ao conjunto de valores "valores_de_guias"
            df_atendimentos = df_atendimentos['GUIA_ATENDIMENTO'].isin(valores_de_guias) 
        else:
            # Cria a mesma variável, mas copiando o dataframe antigo
            df_atendimentos = df_atendimentos.copy()

        # Verifica se a variável "df_filtered" está contida nos elementos locais (contrário de elementos globais) e se é um dataframe não nulo
        if 'df_atendimentos' in locals() and not df_atendimentos.empty:

            merge_df = pd.merge(df_demonstrativo, df_atendimentos, on='GUIA_ATENDIMENTO')

            df_filtrado_periodo = merge_df[(merge_df['DATA_GUIAS'] >= merge_df['CTH_DTHR_INI']) & (merge_df['DATA_GUIAS'] <= merge_df['CTH_DTHR_FIN'])]

            df_tratamento = df_filtrado_periodo[df_filtrado_periodo['HSP_TRAT_INT'] == 'T']

            df_tratamento = df_tratamento[df_tratamento.FAT_NUM != 'nan'].reset_index()

            df_tratamento = df_tratamento.drop(df_tratamento.columns[[0]], axis = 1)

            df_tratamento['FAT_NUM'] = df_tratamento['FAT_NUM'].str.rstrip('.0')

            df_tratamento['FAT_NUM'] = pd.to_numeric(df_tratamento['FAT_NUM'])

            # Mostra na tela o dataframe resultado de todos os processos e filtragens
            st.dataframe(df_tratamento)

            # Cria um "buffer de memória" que pode ser utilizado para leitura de dados de dados binários
            output2 = BytesIO()

            # Transforma o dataframe resultado em formato excel, desconsiderando os índices
            df_tratamento.to_excel(output2, index=False)

            # Esse método movimenta o cursor para o início do buffer, garantindo que a leitura comece deste ponto
            output2.seek(0)

            # Cria um botão de download, responsável por baixar o arquivo "result" em formato excel
            st.download_button(
                label = "Baixar Tratamentos.xls",
                data = output2,
                file_name = f"resultado_atendimentos_filtrado_{datetime.today().strftime('%Y-%m-%d')}.xls",
                mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            
    else:
        # Escreve na tela a mensagem especificada entre aspas 
        st.write("Por favor, faça o upload do arquivo 'Atendimentos'!")

# Elemento que escreve o título da barra de navegação
st.sidebar.title("Navegação")

# Define as páginas possíveis para navegação
page = st.sidebar.radio("", ["INTERNAÇÃO", "TRATAMENTO"])

# Condicional que define qual página estará ativa
if page == "INTERNAÇÃO":
    page_internacao()
else:
    page_tratamento()