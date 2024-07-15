import customtkinter
import tkinter as tk
from PIL import Image
from tkinter import filedialog
import pandas as pd
import datetime

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("750x750")
        self.main_page()


    def read_and_filter_xls(file, column_names, guide_values, date_range):
        df = pd.read_excel(file)
        if 'Guia' in column_names and guide_values:
            df = df[df['Guia'].astype(str).isin(guide_values)]
        if 'Dt item' in column_names and date_range:
            df['Dt item'] = pd.to_datetime(df['Dt item'], dayfirst=True, errors='coerce')
            df = df[(df['Dt item'] >= pd.to_datetime(date_range[0])) & (df['Dt item'] <= pd.to_datetime(date_range[1]))]
        return df

    def main_page(self):
        logo = "logo.png"
        self.logo_image = Image.open(logo)
        self.logo_ctk_image = customtkinter.CTkImage(light_image=self.logo_image, size=(120, 50))
        self.logo_label = customtkinter.CTkLabel(self, image=self.logo_ctk_image, text="")
        self.logo_label.pack(side="top", anchor="nw", padx=10, pady=10)

  
        self.titulo = customtkinter.CTkLabel(self, text="Leitor de planilhas", font=("Arial Rounded MT Bold", 24))
        self.titulo.pack(pady=20)

        self.leitor_arquivos = customtkinter.CTkLabel(self, text="Escolha o arquivo 'Demonstrativo' em formato xls", font=("Arial", 14))
        self.leitor_arquivos.pack(pady=10)

        column_names = ['Guia', 'Dt item']
        guide_values = []
        
        if self.leitor_arquivos is not None:
            self.checkbox_guia = tk.Checkbutton(self.root, text="Filtro Guia", variable=tk.BooleanVar(value=False))
            self.checkbox_guia.pack()
            if self.checkbox_guia:
                guide_values = st.text_input('Digite os valores das guias separados por vírgulas').split(',')

            data = st.checkbox("Filtro Data", value=True)
            date_range = None
            if data:
                date_range = st.date_input(
                    "Selecione o intervalo de datas",
                    value=(datetime(2024, 1, 1).date(), datetime(2024, 12, 31).date())
                )


        self.upload_button = customtkinter.CTkButton(self, text="Carregar Arquivo", command=self.carregar_arquivo)
        self.upload_button.pack(pady=10)

        self.titulo = customtkinter.CTkLabel(self, text="Upload e Filtragem do arquivo ATENDIMENTOS", font=("Arial Rounded MT Bold", 24))
        self.titulo.pack(pady=20)
        self.upload_button2 = customtkinter.CTkButton(self, text="Carregar Arquivo", command=self.carregar_arquivo)
        self.upload_button2.pack(pady=10)
        self.leitor_arquivos = customtkinter.CTkLabel(self, text="Escolha o arquivo 'Atendimentos' em formato xls", font=("Arial", 14))
        self.leitor_arquivos.pack(pady=10)
        

    def carregar_arquivo(self):
        filename = filedialog.askopenfilename(filetypes=[("Arquivos Excel", "*.xlsx;*.xls")])
        if filename:
            print(f"Arquivo selecionado: {filename}")

    





app = App()
app.mainloop()
