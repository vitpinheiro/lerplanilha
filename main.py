# importação de bibliotecas
import pandas as pd
import streamlit as st
from io import BytesIO
from datetime import datetime

# Define a função ler_e_filtrar_xls que recebe um arquivo, nomes de colunas, valores de guias e um intervalo de datas
def ler_e_filtrar_xls(file, nomes_colunas, valores_guias, intervalo_data):
    # df é a variável que armazena o dataframe lido a partir do arquivo excel usando a função pd.read_excel()
    df = pd.read_excel(file)
    
    # Verifica se 'Guia' está na lista de nomes de colunas e se valores_guias não está vazio
    if 'Guia' in nomes_colunas and valores_guias:
        # Filtra o dataframe para manter apenas as linhas onde o valor na coluna 'Guia' está na lista valores_guias
        df = df[df['Guia'].astype(str).isin(valores_guias)]
    # Verifica se 'Dt item' está na lista de nomes de colunas e se intervalo_data não está vazio
    if 'Dt item' in nomes_colunas and intervalo_data:
        # Converte os valores da coluna 'Dt item' para o formato datetime, assumindo que o dia vem antes do mês, ignorando erros
        df['Dt item'] = pd.to_datetime(df['Dt item'], dayfirst=True, errors='coerce')
         # Filtra o dataframe para manter apenas as linhas onde a data está dentro do intervalo especificado
        df = df[(df['Dt item'] >= pd.to_datetime(intervalo_data[0])) & (df['Dt item'] <= pd.to_datetime(intervalo_data[1]))]
    # Retorna o dataframe filtrado
    return df

def main_page():
    # st.image exibe uma imagem
    st.image("LOGO.png", width=150)
    # st.header é o contéudo do cabeçalho, aqui no caso é o título
    st.header('Filtragem de dados sobre Internação')

    # st.file_uploader possibilita a anexagem de um arquivo
    arquivo_carregado = st.file_uploader("Escolha o arquivo 'Demonstrativo' em formato xls")

   
    # nomes_colunas são as colunas filtradas no arquivo
    nomes_colunas = ['Guia', 'Dt item']
    # valores_guias começa como uma lista vazia
    valores_guias = []

    # se algum arquivo for carregado
    if arquivo_carregado is not None:
        # guia é o checkbox de filtragem de guia
        guia = st.checkbox("Filtro Guia", value=False)
        # se o checkbox guia estiver marcado
        if guia:
            # mostra uma caixa para inserir valores de guias, st.text_input exibe uma caixa de texto
            valores_guias = st.text_input('Digite os valores das guias separados por vírgulas').split(',')

        # data é o checkbox de filtragem de data
        data = st.checkbox("Filtro Data", value=True)
        # é utilizado para inicializar a variável e garantir que ela tenha um valor padrão caso o checkbox de filtragem de data não esteja selecionado
        intervalo_data = None
        # se o checkbox de data estiver marcado
        if data:
            # input de data para selecionar o intervalo de datas
            intervalo_data = st.date_input(
                "Selecione o intervalo de datas",
                value=(datetime(2024, 1, 1).date(), datetime(2024, 12, 31).date())
            )

        # st.button é para definir um botão. Esse é de aplicar filtros
        if st.button('Aplicar Filtros'):
            # Se a checkbox de 'Guia' estiver marcada, 'valores_guias' será usada; caso contrário, será None
            guias_selecionadas = valores_guias if guia else None
            # Se a checkbox de 'Data' estiver marcada, 'intervalo_data' será usada; caso contrário, será None
            intervalodata_selecionado = intervalo_data if data else None

            # Chama a função ler_e_filtrar_xls para ler e filtrar o arquivo carregado
            # # - arquivo_carregado: o arquivo XLS/XLSX que foi carregado pelo usuário
            # - nomes_colunas: lista das colunas que serão consideradas para a filtragem ('Guia' e 'Dt item')
            # - guias_selecionadas: valores de guias a serem filtrados, se a checkbox 'guia' estiver marcada; caso contrário, None
            # - intervalodata_selecionado: intervalo de datas a ser filtrado, se a checkbox 'data' estiver marcada; caso contrário, None
            # A função retorna um dataframe filtrado que é armazenado na variável df_filtrado    
            df_filtrado = ler_e_filtrar_xls(arquivo_carregado, nomes_colunas, guias_selecionadas, intervalodata_selecionado)

            # verifica se df_filtrado não é none, antes de tentar exibi-lo ou processá-lo
            if df_filtrado is not None:
                # verifica se df_filtrado é vazio  
                if df_filtrado.empty:
                    # caso seja, exibe que não foi encontrado resultados
                    st.markdown("<h3 style='color: red;'>Resultados não encontrados</h3>", unsafe_allow_html=True)
                # caso contrário, exibe a tabela filtrada
                else:
                    st.write('Tabela filtrada pelos valores selecionados:')
                    # o dataframe  com os valores da coluna Guia e Dt item(planilha Demonstrativo)
                    st.dataframe(df_filtrado[['Guia', 'Dt item']])
               
                    # min_date pega a data mínima de Dt item
                    min_date = df_filtrado['Dt item'].min()
                    # min_date formata a data
                    min_date = pd.to_datetime(min_date, format= "%Y-%m-%d %H:%M:%S")
                    # exibe a menor econtrada
                    st.write(f"A menor data encontrada é: {min_date}")

                    # df_filtrado_by_min_date = df_filtrado[df_filtrado['Dt item'] == min_date][['Guia', 'Dt item']]
                # st.write('Tabela filtrada pela menor data:')
                # st.dataframe(df_filtrado_by_min_date)

    # cado não tenha anexado um arquivo, faça upload  
    else:
        st.write("Por favor, faça o upload de um arquivo XLS/XLSX.")


    # 
    # 
    # Planilha Atendimentos
    st.header('Upload e Filtragem do Arquivo ATENDIMENTOS')
    
    # arquivo_carregado2 é o upload da tabela Atendimentos
    arquivo_carregado2 = st.file_uploader("Escolha o arquivo 'Atendimentos' no formato xls", key="atendimentos")
    
    #se arquivo2 não é none
    if arquivo_carregado2 is not None:
        # ler a planilha
        df = pd.read_excel(arquivo_carregado2)
        # pega o indice original da planilha
        df['Índice Original'] = df.index
        df_filtrado_guia = df[
                df['GUIA_ATENDIMENTO'].isin(df.index) |
                df['GUIA_CONTA'].isin(df.index) |
                df['GIH_NUMERO'].isin(df.index)
            ]

        # Remove pontos das colunas específicas e converte os valores para strings
        df['GUIA_ATENDIMENTO'] = df['GUIA_ATENDIMENTO'].astype(str).str.replace('.', '')
        df['GUIA_CONTA'] = df['GUIA_CONTA'].astype(str).str.replace('.', '')
        df['GIH_NUMERO'] = df['GIH_NUMERO'].astype(str).str.replace('.', '')

        # se for filtrado por guia
        if valores_guias:
            # pega os valores em que GUIA_ATENDIMENTO OU GUIA_CONTA contém valores_guias
            df_filtrado_guia = df[df['GUIA_ATENDIMENTO'].isin(valores_guias) | df['GUIA_CONTA'].isin(valores_guias)]
        # caso contrário, cria uma cópia do DataFrame original df
        else:
            df_filtrado_guia = df.copy()

        # A função locals() em Python retorna um dicionário contendo todas as variáveis locais do escopo atual
        # está acessando a variável 'df_filtrado', verificando se ela está definida no escopo
        # verifica se df_filtrado não está vazio
        if 'df_filtrado'in locals() and not df_filtrado.empty:
            
            # pega a data mínima de Dt item e a converte
            min_date = df_filtrado['Dt item'].min()
            min_date = pd.to_datetime(min_date, format="%Y-%m-%d %H:%M:%S")
        
            # converte CTH_DTHR_INI E CTH_DTHR_FIN
            df_filtrado_guia['CTH_DTHR_INI'] = pd.to_datetime(df_filtrado_guia['CTH_DTHR_INI'], errors='coerce')
            df_filtrado_guia['CTH_DTHR_FIN'] = pd.to_datetime(df_filtrado_guia['CTH_DTHR_FIN'], errors='coerce')



            # # Se o DataFrame filtrado contém apenas uma linha
            # if len(df_filtrado_guia) == 1:
            #     # Nesse caso, não é necessário aplicar mais filtros.
            #     # Apenas atribui o DataFrame original à nova variável df_filtrado2.
            #     df_filtrado2 = df_filtrado_guia
            # # caso contrário, aplica um filtro adicional com base na data mínima
            # # Onde inclui apenas as linhas onde a data mínima está dentro do intervalo definido pelas colunas 'CTH_DTHR_INI' e 'CTH_DTHR_FIN'
            # else:   
            #     df_filtrado_guia = df_filtrado_guia.loc[
            #         (df_filtrado_guia['CTH_DTHR_INI'] <= min_date) &
            #         (min_date <= df_filtrado_guia['CTH_DTHR_FIN'])
            #     ]

            

            # pega as linhas apenas onde GUIA_ATENDIMENTO FOR IGUAL A GIH_NUMERO
            df_filtrado2 = df_filtrado_guia[df_filtrado_guia['GUIA_ATENDIMENTO'] == df_filtrado_guia['GIH_NUMERO']]
            df_filtrado2 = df_filtrado2[df_filtrado2['CTH_NUM'] != 0]
            # as colunas que serão exibidas
            df_filtrado2 = df_filtrado2[['GUIA_ATENDIMENTO','GUIA_CONTA','HSP_NUM', 'HSP_PAC', 'CTH_NUM', 'FAT_SERIE', 'FAT_NUM', 'NFS_SERIE', 'NFS_NUMERO', 'CTH_DTHR_INI', 'CTH_DTHR_FIN']]
            # conversão para string
            df_filtrado2['NFS_NUMERO'] = df_filtrado2['NFS_NUMERO'].astype(str)
            df_filtrado2['HSP_PAC'] = df_filtrado2['HSP_PAC'].astype(str)
            df_filtrado2['FAT_NUM'] = df_filtrado2['FAT_NUM'].astype(str)

            # renomeando nomes das colunas
            df_filtrado2 = df_filtrado2.rename(columns={'HSP_NUM':'IH', 'HSP_PAC':'REGISTRO', 'CTH_NUM':'CONTA', 'FAT_SERIE':'PRE.S', 'FAT_NUM':'PRE.NUM', 'NFS_SERIE':'FAT.S', 'NFS_NUMERO':'FAT.NUM', 'CTH_DTHR_INI':'DATA_INICIO', 'CTH_DTHR_FIN':'DATA_FIM'})
       
            # st.dataframe(df_filtrado2)
            
            # Merge para encontrar apenas as linhas em comum com 'GUIA_ATENDIMENTO'
            result = pd.merge(df_filtrado[['Guia', 'Dt item']], df_filtrado2, left_on='Guia', right_on='GUIA_ATENDIMENTO', how='inner')
            
            # retira duplicações
            result.drop_duplicates(subset=['Guia'], keep='first', inplace=True)

            # exibe o dataframe filtrado
            st.dataframe(result)


            # Cria um buffer em memória para armazenar o arquivo Excel
            output2 = BytesIO()
            # Salva o DataFrame 'result' como um arquivo Excel no buffer
            result.to_excel(output2, index=False)
            # Garante que o Streamlit possa ler o conteúdo do buffer a partir do início.
            output2.seek(0)
            # Cria um botão de download no Streamlit
            st.download_button(
                label="Baixar arquivo Excel", # Texto exibido no botão
                data=output2,  # Dados do arquivo Excel a serem baixados
                file_name=f"resultado_atendimentos_filtrado_{datetime.today().strftime('%Y-%m-%d')}.xlsx", # Nome do arquivo para download, com a data atual no formato YYYY-MM-DD
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" # Nome do arquivo para download, com a data atual no formato YYYY-MM-DD
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
