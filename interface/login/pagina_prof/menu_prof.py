import tkinter as tk
from tkinter import Label, Tk, PhotoImage
from util.db import conexaoBanco
import os
from util.config import cor0, texto1, cor3, config_botao, config_botao_cursos, config_text_box
from interface.login.pagina_prof.menus_prof import info
from interface.login import editar_perfil

# variaveis
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

    # Margem do canvas
    margem_x = 70
    margem_y = 50

    # Espaçamento entre os botões
    espaco_x = 150
    espaco_y = 100

    try:
        # Conecta ao banco usando o util.db
        conexao = conexaoBanco()
        if conexao:
            cursor = conexao.cursor()

            # Recupera o perfil do usuário
            cursor.execute("SELECT id_perfis FROM perfis WHERE login = %s", (Perfil,))
            id_perfis = cursor.fetchone()

            if id_perfis is not None:
                id_perfis = id_perfis[0]  # Extrai o valor de id_perfis da tupla

                # Recupera os cursos associados ao perfil
                cursor.execute("SELECT id_curso FROM inscricoes WHERE id_perfis = %s", (id_perfis,))
                ids_cursos = cursor.fetchall()

                if ids_cursos:
                    # Extrai os IDs de cursos de forma plana
                    ids_cursos = [id_curso[0] for id_curso in ids_cursos]

                    # Recupera os nomes dos cursos
                    cursor.execute("SELECT nome FROM cursos WHERE id_curso IN (%s)" % ",".join(["%s"] * len(ids_cursos)),
                                   ids_cursos)
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


def j_editar_perfil(perfil):
    editar_perfil.Editar_perfil(perfil)


# tela de login
def sair(JMP):
    JMP.quit()
    JMP.destroy()
    from interface.login.paginaLogin import LoginUsuario
    LoginUsuario()


def iniciar(perfil):
    JMP: Tk = tk.Tk()
    JMP.title("Gestão de Cursos UNI-CEUB")
    JMP.geometry("600x350")
    JMP.configure(bg=cor0)
    JMP.resizable(False, False)
    global x
    global Perfil
    Perfil = perfil
    x = JMP
    # Imagem CEUB
    diretorio_atual = os.path.dirname(__file__)
    caminho_imagem = os.path.join(diretorio_atual, "..", "..", "imagens", "uniceub.png")
    logo_img = PhotoImage(file=caminho_imagem)

    logo_label = tk.Label(JMP, image=logo_img, bd=0, relief="solid")
    logo_label.place(x=10, y=0)

    # local dos botoes de menu
    menu = tk.Canvas(JMP, width=110, height=300, bg=cor0, bd=0, highlightthickness=0)
    menu.place(x=17, y=45)

    # local dos botoes de curso
    canvas = tk.Canvas(JMP, width=445, height=265, bg=cor3, bd=0, highlightthickness=1, highlightbackground="black")
    canvas.place(x=145, y=75)

    # Adicionando o evento de rolagem no local dos cursos
    canvas.bind_all("<MouseWheel>", lambda event: rolar_canvas(event, canvas))

    # botoes do menu
    botao_Info = tk.Button(JMP, text="Info", **config_botao, command=lambda: info_curso())
    menu.create_window(55, 54, window=botao_Info)

    botao_Editar_perfil = tk.Button(JMP, text="Editar perfil", **config_botao, command=lambda: j_editar_perfil(perfil))
    menu.create_window(55, 108, window=botao_Editar_perfil)

    botao_Sair = tk.Button(JMP, text="Sair", **config_botao, command=lambda: sair(JMP))
    menu.create_window(55, 162, window=botao_Sair)

    # Caixa de pesquisa
    pesquisa_var = tk.StringVar()
    pesquisa = tk.Entry(JMP, textvariable=pesquisa_var, **config_text_box, width=49)
    pesquisa.place(x=145, y=15)

    # Monitorar a barra de pesquisa e atualizar os botões quando o usuário digitar
    pesquisa.bind("<KeyRelease>", lambda event: pesquisar(event, canvas, pesquisa_var))

    # Gerar os botões para os cursos
    gerar_botoes(canvas)
    JMP.mainloop()
