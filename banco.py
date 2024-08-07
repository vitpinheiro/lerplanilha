import pyodbc
import pandas as pd
import datetime
import os

agora = datetime.datetime.now()

agora = agora.strftime('%d-%m-%Y_%Hh%Mm%Ss')

def consulta():
    # Configurações da conexão
    server = r'10.1.3.196,50000'  # Substitua pelo nome do seu servidor SQL Server
    database = 'SMARTTESTE'  # Substitua pelo nome do seu banco de dados
    username = 'smrtusr'  # Substitua pelo seu nome de usuário
    password = 'SMART2023#'  # Substitua pela sua senha


    # String de conexão
    connection_string = f'DRIVER=ODBC Driver 17 for SQL Server;SERVER={server};DATABASE={database};UID={username};PWD={password};'

    query = """
    SELECT 
    distinct 
    HSP.HSP_NUM,
    HSP.HSP_PAC,
    PAC.PAC_NOME,
    HSP.HSP_DTHRE,
    HSP.HSP_DTHRA,
    HSP.HSP_TRAT_INT,
    CTH.CTH_NUM,
    CTH.CTH_DTHR_INI,
    CTH.CTH_DTHR_FIN,
    GIH.GIH_TISS_GUIA_PRINCIPAL AS 'GUIA_ATENDIMENTO',
    CTH.CTH_CTLE_CNV AS 'GUIA_CONTA',
    CNV.CNV_COD,
    CNV.CNV_NOME,
    GIH.GIH_NUMERO,
    GIH.GIH_DTHR_INI,
    GIH.GIH_DTHR_FIM,
    GIH.GIH_DTHR_VALID,
    FAT.FAT_SERIE,
    FAT.FAT_NUM
    FROM 
    HSP 
    left join 
    gih on gih.GIH_HSP_NUM = hsp.hsp_num and gih.GIH_PAC_REG = hsp.hsp_pac
        LEFT JOIN 
    CTH ON CTH.CTH_HSP_NUM = HSP.HSP_NUM AND CTH.CTH_PAC_REG = HSP.HSP_PAC
        LEFT JOIN
    FAT ON CTH.CTH_FAT_SERIE = FAT.FAT_SERIE AND CTH.CTH_FAT_NUM = FAT.FAT_NUM,
    CNV,
    PAC
    WHERE
    CTH.CTH_CNV_COD = CNV_COD AND
    HSP.HSP_PAC = pac.pac_reg AND
    HSP.HSP_DTHRE BETWEEN GETDATE() - 720 AND GETDATE() AND
    CNV.CNV_COD = '2' 


    UNION ALL

    SELECT 
    distinct
    HSP.HSP_NUM,
    HSP.HSP_PAC,
    PAC.PAC_NOME,
    HSP.HSP_DTHRE,
    HSP.HSP_DTHRA,
    HSP.HSP_TRAT_INT,
    0,
    hsp.HSP_DTHRE,
    hsp.HSP_DTHRA,
    GIH.GIH_TISS_GUIA_PRINCIPAL AS 'GUIA_ATENDIMENTO',
    '0',
    CNV.CNV_COD,
    CNV.CNV_NOME,
    GIH.GIH_NUMERO,
    GIH.GIH_DTHR_INI,
    GIH.GIH_DTHR_FIM,
    GIH.GIH_DTHR_VALID,
    FAT.FAT_SERIE,
    FAT.FAT_NUM
    FROM 
    HSP 
    left join 
    gih on gih.GIH_HSP_NUM = hsp.hsp_num and gih.GIH_PAC_REG = hsp.hsp_pac
        LEFT JOIN 
    smm ON smm.SMM_HSP_NUM= HSP.HSP_NUM AND smm.SMM_PAC_REG = HSP.HSP_PAC
        LEFT JOIN
    FAT ON smm.SMM_FAT_SERIE = FAT.FAT_SERIE AND smm.SMM_FAT = FAT.FAT_NUM,
    CNV,
    PAC
    WHERE
    HSP.HSP_CNV = CNV_COD AND
    HSP.HSP_PAC = pac.pac_reg AND
    HSP.HSP_TRAT_INT = 'T' AND
    HSP.HSP_DTHRE BETWEEN GETDATE() - 720 AND GETDATE() AND
    CNV.CNV_COD = '2' 
    order by
    HSP_PAC,
    hsp_num
    """

    try:
    # Conectando ao banco de dados
        connection = pyodbc.connect(connection_string)

        # Lendo a consulta diretamente para um DataFrame
        df = pd.read_sql(query, connection)

        pasta = os.path.join(os.environ['USERPROFILE'], 'Downloads')
        nome_arquivo = f'Atendimentos_{agora}.xlsx'
        caminho_arquivo = os.path.join(pasta, nome_arquivo)

        df.to_excel(caminho_arquivo, index=False)
        print(f"DataFrame salvo em '{caminho_arquivo}'")
        
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        input('Pressione qualquer tecla para encerrar: ')

    finally:
        # Fechando a conexão
        if 'connection' in locals():
            connection.close()
    return df

df = consulta()
