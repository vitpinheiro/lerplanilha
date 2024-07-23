from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

class SidebarApp(App):
    def build(self):
        # Layout principal
        main_layout = BoxLayout(orientation='horizontal')
        
        # Sidebar
        sidebar = BoxLayout(orientation='vertical', size_hint=(0.2, 1))
        
        # Adicionando widgets à sidebar
        sidebar.add_widget(Button(text='Botão 1'))
        sidebar.add_widget(Button(text='Botão 2'))
  
        
        # Conteúdo principal
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text='Conteúdo Principal', font_size=24))
        
        # Adicionando sidebar e conteúdo principal ao layout principal
        main_layout.add_widget(sidebar)
        main_layout.add_widget(content)
        
        return main_layout

if __name__ == '__main__':
    SidebarApp().run()
