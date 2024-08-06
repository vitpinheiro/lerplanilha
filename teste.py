import pyexcel as p

file = r"C:\Users\pedronobrega\Desktop\Projeto_Leitor_Planilha\Demonstrativo original 04-2024.xls"

p.save_book_as(file_name = file, dest_file_name='Demonstrativo.xlsx')