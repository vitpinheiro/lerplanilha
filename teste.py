import customtkinter as ctk
from tkinter import filedialog

# Função para abrir o diálogo de seleção de arquivos
def open_file():
    # Abrir o diálogo de seleção de arquivos
    file_path = filedialog.askopenfilename(
        title="Selecione um arquivo",
        filetypes=(("Arquivos de Texto", "*.txt"), ("Todos os Arquivos", "*.*"))
    )
    
    # Atualizar o texto do label com o caminho do arquivo selecionado
    if file_path:
        file_label.configure(text=f"Arquivo Selecionado: {file_path}")

# Função principal para criar a aplicação
def main():
    # Criar a janela principal
    root = ctk.CTk()  # Usa CTk para criar a janela

    # Configurar o tamanho da janela
    root.geometry("800x600")  # Tamanho da janela: largura x altura

    # Criar um botão para abrir o diálogo de seleção de arquivos
    open_button = ctk.CTkButton(root, text="Abrir Arquivo", command=open_file)
    open_button.place(x=10, y=10)  # Posicionar o botão

    # Criar um label para mostrar o caminho do arquivo selecionado
    global file_label
    file_label = ctk.CTkLabel(root, text="Nenhum arquivo selecionado")
    file_label.place(x=10, y=50)  # Posicionar o label

    # Iniciar o loop principal da aplicação
    root.mainloop()

if __name__ == "__main__":
    main()