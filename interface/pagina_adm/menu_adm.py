import tkinter as tk
from tkinter import Label
import info
import editar
import criar


#variaveis
curso_selecionado = ""
cor0= '#1C1C1C'
cor1= '#363636'
texto= '#DCDCDC'
cor3= '#4F4F4F'

#test
cursos = [
    "Curso 1", "Curso 2", "Curso 3", "Curso 4", "Curso 5",
    "Curso 6", "Curso 7", "Curso 8", "Curso 9", "Curso 10",
    "Curso 11", "Curso 12", "Curso 13", "Curso 14", "Curso 15",
]

#config botoes
config_botao = {
    'font': ("Arial", 13, "bold"),
    'bg': cor1,
    'fg': texto,
    'activebackground': cor3,
    'relief': "flat",
    'width': 12,
    'height': 2
}

#config cursos botaos
config_botao_cursos = {
    'font': ("Arial", 10, "bold"),
    'bg': cor1,
    'fg': texto,
    'activebackground': cor3,
    'relief': "flat",
    'width': 12,
    'height': 4
}

#config caixa de texto
config_text_box = {
    'font': ("Arial", 13, "bold"),
    'bg': cor3,
    'fg': texto,
    'relief': "flat",
    'width': 49
}

#memoriza o curso selecionado
def salvar_curso(nome):
    global curso_selecionado
    curso_selecionado = nome
    texto_informativo = tk.Label(
        JGC,
        text=f"Curso selecionado: {nome}",
        font=("Arial", 13, "bold"),
        fg=texto,
        bg=cor0,
    )
    texto_informativo.place(x=145, y=43)
    print(f"Curso selecionado: {nome}")

#rolagem para o Canva
def rolar_canvas(event, canvas):
    if event.delta > 0:
            canvas.yview_scroll(-1, "units")
    else:
            canvas.yview_scroll(1, "units")


#gerrador de botoes de curso
def gerar_botoes(canvas, termo_pesquisa=""):
    # Limpar os botões anteriores
    canvas.delete("all")
    # Definir a quantidade de botões por linha
    colunas = 3

    # margem do canva
    margem_x = 70
    margem_y = 50

    # Espaçamento entre os botões
    espaco_x = 150
    espaco_y = 100

    # Filtrar os cursos com base no termo de pesquisa
    cursos_filtrados = [curso for curso in cursos if termo_pesquisa.lower() in curso.lower()]

    for i, curso in enumerate(cursos_filtrados):
        # Calcular posição (x, y) baseado no índice
        linha = i // colunas
        coluna = i % colunas

        # Calcular a posição (x, y) para o botão
        x = margem_x + (coluna * espaco_x)
        y = margem_y + (linha * espaco_y)

        # Criar o botão com o nome do curso
        botao = tk.Button(canvas, text=curso,**config_botao_cursos, command=lambda nome=curso: salvar_curso(nome))
        canvas.create_window(x, y, window=botao)

        # Adicionar o nome do curso abaixo do botão
        canvas.create_text(x, y + 50, text=curso, fill=texto,
                           font=("Arial", 8,"bold"))

#QUANDO APERTAR (ENTER) NA CAIXA DE PESQUISA
def pesquisar(canvas):
    # Obtém o texto da caixa de pesquisa
    termo = pesquisa_var.get()
    # Atualiza os botões de curso com base no termo de pesquisa
    gerar_botoes(canvas, termo)

#Janela de informações do curso
def info_curso(nome):
    if nome != '':
        info.Info(cor0, texto, nome)
    else:
        print("Nenhum curso foi selecionado!")


#Janela criar
def j_criar():
    criar.Criar(cor0, texto, cor3)
    print(f"abriua janela de criar")

#Janela criar
def j_editar(nome):
    if nome != '':
        editar.Editar(cor0, texto, nome, cor3)
    else:
        print("Nenhum curso foi selecionado!")

#tela de login
def sair():

    print(f"voltar para tela de login")

#janela Gestão de Cursos UNI-CEUB

#configuraçoes da janela

JGC = tk.Tk()
JGC.title("Gestão de Cursos UNI-CEUB")
JGC.geometry("600x350")
JGC.configure(bg=cor0)
JGC.resizable(False, False)

#local dos botoes de menu
menu = tk.Canvas(JGC, width=110, height=300, bg=cor0, bd=0, highlightthickness=0)
menu.place(x=17, y=38)

#local dos botoes de curso
canvas = tk.Canvas(JGC, width=445, height=265, bg=cor3, bd=0, highlightthickness=0)
canvas.place(x=145, y=75)

# Adicionando o evento de rolagem no local dos cursos
canvas.bind_all("<MouseWheel>", lambda event, canvas=canvas: rolar_canvas(event, canvas))

#botoes do menu
botao_Info = tk.Button(JGC, text="Info", **config_botao, command=lambda: info_curso(curso_selecionado))
menu.create_window(55, 63, window=botao_Info)

botao_Criar = tk.Button(JGC, text="Criar Curso", **config_botao, command= j_criar)
menu.create_window(55, 135, window=botao_Criar)

botao_Editar = tk.Button(JGC, text="Editar Curso", **config_botao, command=lambda: j_editar(curso_selecionado))
menu.create_window(55, 206, window=botao_Editar)

botao_Sair = tk.Button(JGC, text="Sair", **config_botao, command=lambda: sair)
menu.create_window(55, 276, window=botao_Sair)

# Gerar os botões para os cursos
gerar_botoes(canvas)

# Caixa de pesquisa
pesquisa_var = tk.StringVar()
pesquisa = tk.Entry(JGC, textvariable=pesquisa_var, **config_text_box)
pesquisa.place(x=145, y=15)
texto_informativo: Label = tk.Label(
        JGC,
        text=f"Cursos:",
        font=("Arial", 13, "bold"),
        fg=texto,
        bg=cor0,
    )
texto_informativo.place(x=145, y=43)

# Monitorar a barra de pesquisa e atualizar os botões quando o usuário digitar
pesquisa.bind("<KeyRelease>", lambda event, canvas=canvas: pesquisar(event, canvas))

JGC.mainloop()
