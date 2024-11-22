import tkinter as tk


class gestaoCuros:
    
    janela = tk.Tk()
    janela.title('Gestão de Cursos')
    janela.geometry('300x100')
    janela.resizable(False, False) # Comando para tirar a responsividade da sua janela
    janela.iconbitmap('imagens/favicon.ico') # Comando para adcionar uma imagem no título da janela

    labelJanela = tk.Label(janela, text='Teste de label')
    labelJanela.pack()

    janela.mainloop()
    