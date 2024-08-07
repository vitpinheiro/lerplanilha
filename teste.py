import pandas as pd
import io

# Função para converter .xls para .xlsx
def convert_xls_to_xlsx(file_path):
    # Ler o arquivo .xls
    df = pd.read_excel(file_path, engine='xlrd')
    
    # Criar um objeto BytesIO para armazenar o arquivo .xlsx em memória
    output = io.BytesIO()

    # Salvar o DataFrame como um arquivo .xlsx no objeto BytesIO
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    
    # Mover o ponteiro do objeto BytesIO para o início
    output.seek(0)

    # Retornar o objeto BytesIO
    return output

file_path = r'C:\Users\pedronobrega\Desktop\Projeto_Leitor_Planilha\Planilha_Teste.xls'
xlsx_file = convert_xls_to_xlsx(file_path)

# Agora você pode usar `xlsx_file` como um arquivo .xlsx em memória
# Exemplo: ler o arquivo xlsx em memória de volta para um DataFrame
df_from_xlsx = pd.read_excel(xlsx_file)

# Verificar os dados
print(df_from_xlsx)

