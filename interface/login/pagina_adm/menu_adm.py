import tkinter as tk
from tkinter import Label, Tk, PhotoImage
from util.db import conexaoBanco
import os
from util.config import cor0, texto1, cor3, config_botao, config_botao_cursos, config_text_box
from interface.login.pagina_adm.menus_adm import info
from interface.login.pagina_adm.menus_adm import editar
from interface.login import editar_perfil
from interface.login.pagina_adm.menus_adm import criar

texto_informativo = None
curso_selecionado = None

# memoriza o curso selecionado
def salvar_curso(nome):
    global curso_selecionado, texto_informativo
    curso_selecionado = nome
    if texto_informativo:
        texto_informativo.config(text=f"Cursos: {nome}")
    else:
        texto_informativo = Label(x, text=f"Cursos: {nome}", font=("Arial", 13, "bold"), fg=texto1, bg=cor0)
        texto_informativo.place(x=145, y=43)


# rolagem para o Canva
def rolar_canvas(event, canvas):
    if event.delta > 0:
        canvas.yview_scroll(-1, "units")
    else:
        canvas.yview_scroll(1, "units")


# gerrador de botoes de curso
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

    try:
        conexao = conexaoBanco()
        if conexao:
            cursor = conexao.cursor()

            cursor.execute("SELECT nome FROM curso")
            resultados = cursor.fetchall()

            # Filtrar os cursos com base no termo de pesquisa
            cursos_filtrados = [curso[0] for curso in resultados if termo_pesquisa.lower() in curso[0].lower()]

            # Quantidade de linhas necessárias
            linhas = (len(cursos_filtrados) + colunas - 1) // colunas  # Arredonda para cima

            # Calcular a altura total necessária
            altura_total = margem_y + (linhas * espaco_y)

            for i, curso in enumerate(cursos_filtrados):
                # Calcular posição (x, y) baseado no índice
                linha = i // colunas
                coluna = i % colunas

                # Calcular a posição (x, y) para o botão
                x = margem_x + (coluna * espaco_x)
                y = margem_y + (linha * espaco_y)

                # Criar o botão com o nome do curso
                botao = tk.Button(canvas, text=curso, **config_botao_cursos,
                                  command=lambda nome=curso: salvar_curso(nome))
                canvas.create_window(x, y, window=botao)

            # Ajustar a região de rolagem do canvas
            canvas.config(scrollregion=(0, 0, canvas.winfo_width(), altura_total))
            # Fecha a conexão e o cursor
            cursor.close()
            conexao.close()
        else:
            print("Erro", "Não foi possível conectar ao banco de dados.")
    except Exception as e:
        print("Erro", f"Ocorreu um erro ao salvar: {e}")


def pesquisar(event, canvas, pesquisa_var=None):
    termo = pesquisa_var.get()
    gerar_botoes(canvas, termo)


def info_curso():
    if curso_selecionado:
        info.Info(curso_selecionado)
    else:
        print("Nenhum curso foi selecionado!")


def j_criar():
    criar.Criar()


# Janela criar
def j_editar():
    if curso_selecionado:
        editar.Editar(curso_selecionado)
    else:
        print("Nenhum curso foi selecionado!")


def j_editar_perfil(perfil):
    editar_perfil.Editar_perfil(perfil)


# tela de login
def sair(JDA):
    JDA.quit()
    JDA.destroy()
    from interface.login.paginaLogin import LoginUsuario
    LoginUsuario()


def iniciar(perfil):
    JDA: Tk = tk.Tk()
    JDA.title("Gestão de Cursos UNI-CEUB")
    JDA.geometry("600x350")
    JDA.configure(bg=cor0)
    JDA.resizable(False, False)
    global x
    x = JDA
    # Imagem CEUB
    diretorio_atual = os.path.dirname(__file__)
    caminho_imagem = os.path.join(diretorio_atual, "..", "..", "imagens", "uniceub.png")
    logo_img = PhotoImage(file=caminho_imagem)

    logo_label = tk.Label(JDA, image=logo_img, bd=0, relief="solid")
    logo_label.place(x=10, y=0)

    # local dos botoes de menu
    menu = tk.Canvas(JDA, width=110, height=300, bg=cor0, bd=0, highlightthickness=0)
    menu.place(x=17, y=45)

    # local dos botoes de curso
    canvas = tk.Canvas(JDA, width=445, height=265, bg=cor3, bd=0, highlightthickness=1, highlightbackground="black")
    canvas.place(x=145, y=75)

    # Adicionando o evento de rolagem no local dos cursos
    canvas.bind_all("<MouseWheel>", lambda event: rolar_canvas(event, canvas))

    # botoes do menu
    botao_Info = tk.Button(JDA, text="Info", **config_botao, command=lambda: info_curso())
    menu.create_window(55, 54, window=botao_Info)

    botao_Criar = tk.Button(JDA, text="Criar Curso", **config_botao, command=j_criar)
    menu.create_window(55, 110, window=botao_Criar)

    botao_Editar = tk.Button(JDA, text="Editar Curso", **config_botao, command=lambda: j_editar())
    menu.create_window(55, 164, window=botao_Editar)

    botao_Editar_perfil = tk.Button(JDA, text="Editar perfil", **config_botao, command=lambda: j_editar_perfil(perfil))
    menu.create_window(55, 220, window=botao_Editar_perfil)

    botao_Sair = tk.Button(JDA, text="Sair", **config_botao, command=lambda: sair(JDA))
    menu.create_window(55, 274, window=botao_Sair)

    # Caixa de pesquisa
    pesquisa_var = tk.StringVar()
    pesquisa = tk.Entry(JDA, textvariable=pesquisa_var, **config_text_box, width=49)
    pesquisa.place(x=145, y=15)

    # Monitorar a barra de pesquisa e atualizar os botões quando o usuário digitar
    pesquisa.bind("<KeyRelease>", lambda event: pesquisar(event, canvas, pesquisa_var))

    # Gerar os botões para os cursos
    gerar_botoes(canvas)
    JDA.mainloop()
