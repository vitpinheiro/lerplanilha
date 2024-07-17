import customtkinter
from PIL import Image

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.configure(fg_color="white")
        self.title("Teste Tkinter")
        self.geometry("1000x650")

        # Adiciona a imagem da logo do hospital
        my_image = customtkinter.CTkImage(light_image=Image.open(r"C:\Users\pedronobrega\Desktop\Ler_Planilhas_Novo\LOGO.png"), dark_image=Image.open(r"C:\Users\pedronobrega\Desktop\Ler_Planilhas_Novo\LOGO.png"), size=(75, 75))
        
        # Cria um botão com a imagem da logo que redireciona para o site do hospital
        botao_logo = customtkinter.CTkButton(self, text=None, image=my_image, height=60, fg_color='transparent', width=60, hover=False, anchor='nw')
        botao_logo.place(x=30, y=30)

        # Cria a label referente ao título da página
        label_principal = customtkinter.CTkLabel(self, text = "LEITOR DE PLANILHAS", fg_color="transparent", height=130, font = ("Arial Rounded MT Bold", 35, "bold"))
        label_principal.pack()

        # Label "Filtragem de dados sobre internação"
        label_primeira_filtragem = customtkinter.CTkLabel(self, text = "Filtragem de dados sobre Internação", fg_color = "transparent", font = ("Helvetica", 25, "bold"))
        label_primeira_filtragem.place(x=30, y = 150)

        # Label instrutiva para inserção de arquivo "Insira o arquivo Demonstrativo"
        label_demonstrativo = customtkinter.CTkLabel(self, text = "Escolha o arquivo 'Demonstrativo' em formato xls", fg_color='transparent', font = ("Helvetica", 14, "bold"), text_color='gray')
        label_demonstrativo.place(x = 30, y = 185)


    # add methods to app
    def button_click(self):
        print("button click")


app = App()
app.mainloop()