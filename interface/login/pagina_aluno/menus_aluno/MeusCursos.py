import tkinter as tk
from tkinter import ttk, PhotoImage, messagebox
from util.db import conexaoBanco  # Certifique-se de ter a classe SQL configurada
from interface.login.pagina_aluno.menus_aluno.DadosUsuario import abrir_dados_usuario
from interface.login.pagina_aluno.menus_aluno.PaginaCurso import abrir_pagina_curso
import os

def meusCursos(perfil):

    def desinscrever_curso(tree, login_usuario):
        """
        Remove a inscrição do curso selecionado no Treeview para o usuário logado.
        """
        try:
            # Obter o item selecionado no Treeview
            selected_item = tree.focus()
            if not selected_item:
                messagebox.showwarning("Seleção Inválida", "Por favor, selecione um curso para se desinscrever.")
                return

            # Obter os valores da linha selecionada
            valores = tree.item(selected_item, "values")
            if not valores:
                messagebox.showerror("Erro", "Erro ao obter os dados do curso.")
                return

            # Extrair o identificador do curso
            identificador = valores[0]  # Supondo que o identificador está na primeira coluna

            # Conectar ao banco de dados
            conn = conexaoBanco()
            cursor = conn.cursor()

            # Consultar o ID do perfil do usuário com base no login
            query_perfil = "SELECT id_perfis FROM perfis WHERE login = %s"
            cursor.execute(query_perfil, (login_usuario,))
            resultado_perfil = cursor.fetchone()

            if not resultado_perfil:
                messagebox.showerror("Erro", "Usuário não encontrado.")
                cursor.close()
                conn.close()
                return

            id_perfil = resultado_perfil[0]

            # Remover a inscrição do curso
            query_delete = """
                DELETE FROM inscricoes
                WHERE id_perfis = %s AND id_curso = %s
            """
            cursor.execute(query_delete, (id_perfil, identificador))
            conn.commit()

            # Verificar se a inscrição foi realmente removida
            if cursor.rowcount == 0:
                messagebox.showerror("Erro", "Não foi possível desinscrever-se do curso.")
            else:
                messagebox.showinfo("Sucesso", f"Você se desinscreveu do curso com ID {identificador}.")
                # Remover o curso do Treeview
                tree.delete(selected_item)

            # Fechar conexão
            cursor.close()
            conn.close()

        except Exception as e:
            messagebox.showerror("Erro ao Desinscrever", f"Ocorreu um erro ao tentar desinscrever-se do curso.\n\n{e}")

    def abrir_curso(tree, login_usuario):
        """
        Abre os detalhes do curso selecionado no Treeview, incluindo informações das tabelas 'cursos' e 'inscricoes'.
        """
        try:
            # Obter o item selecionado no Treeview
            selected_item = tree.focus()
            if not selected_item:
                messagebox.showwarning("Seleção Inválida", "Por favor, selecione um curso.")
                return

            # Obter os valores da linha selecionada
            valores = tree.item(selected_item, "values")
            if not valores:
                messagebox.showerror("Erro", "Erro ao obter os dados do curso.")
                return

            # Extrair o identificador do curso
            identificador = valores[0]  # Supondo que o identificador está na primeira coluna

            # Conectar ao banco de dados
            conn = conexaoBanco()
            cursor = conn.cursor()

            # Consultar informações do curso na tabela 'cursos'
            query_curso = """
                SELECT c.nome, c.carga_horaria, c.descricao
                FROM cursos c
                WHERE c.id_curso = %s
            """
            cursor.execute(query_curso, (identificador,))
            curso_detalhes = cursor.fetchone()

            if not curso_detalhes:
                messagebox.showerror("Erro", "Curso não encontrado.")
                cursor.close()
                conn.close()
                return

            titulo, carga_horaria, descricao = curso_detalhes

            # Consultar informações do curso na tabela 'inscricoes'
            query_inscricao = """
                SELECT i.nota_aluno, i.presenca_aluno
                FROM inscricoes i
                JOIN perfis p ON i.id_perfis = p.id_perfis
                WHERE i.id_curso = %s AND p.login = %s
            """
            cursor.execute(query_inscricao, (identificador, login_usuario))
            inscricao_detalhes = cursor.fetchone()

            if not inscricao_detalhes:
                nota = "N/A"
                presenca = "N/A"
            else:
                nota, presenca = inscricao_detalhes

            # Fechar conexão
            cursor.close()
            conn.close()

            # Criar uma nova janela para exibir os detalhes do curso
            detalhes_janela = tk.Toplevel()
            detalhes_janela.title(f"Detalhes do Curso: {titulo}")
            detalhes_janela.geometry("400x400")

            # Exibir os detalhes do curso
            tk.Label(detalhes_janela, text="Detalhes do Curso", font=("Arial", 16, "bold")).pack(pady=10)
            tk.Label(detalhes_janela, text=f"Título: {titulo}", font=("Arial", 12)).pack(pady=5)
            tk.Label(detalhes_janela, text=f"Carga Horária: {carga_horaria} horas", font=("Arial", 12)).pack(pady=5)
            tk.Label(detalhes_janela, text=f"Descrição: {descricao}", font=("Arial", 12), wraplength=350,
                     justify="left").pack(pady=5)
            tk.Label(detalhes_janela, text=f"Nota: {nota}", font=("Arial", 12)).pack(pady=5)
            tk.Label(detalhes_janela, text=f"Presença: {presenca} horas", font=("Arial", 12)).pack(pady=5)

            # Botão para fechar a janela de detalhes
            tk.Button(detalhes_janela, text="Fechar", command=detalhes_janela.destroy).pack(pady=20)

        except Exception as e:
            messagebox.showerror("Erro ao Abrir Curso", f"Ocorreu um erro ao tentar abrir os detalhes do curso.\n\n{e}")

    def consultar_cursos_inscritos(tree, login_usuario):
        """
        Consulta os cursos em que o usuário está inscrito, utilizando o login, e exibe na Treeview.
        """
        try:
            # Conectar ao banco de dados
            conn = conexaoBanco()
            cursor = conn.cursor()

            # Imprima o login para garantir que ele está correto
            print(f"Login do usuário: {login_usuario}")

            # Consulta SQL para buscar os cursos inscritos pelo usuário
            query = """
                SELECT c.id_curso AS identificador,
                       c.nome AS titulo,
                       c.carga_horaria AS carga_horaria,
                       CASE 
                           WHEN c.vagas > 0 THEN 'Disponível'
                           ELSE 'Indisponível'
                       END AS disponibilidade
                FROM inscricoes i
                JOIN cursos c ON i.id_curso = c.id_curso
                JOIN perfis p ON i.id_perfis = p.id_perfis
                WHERE p.login = %s
            """
            cursor.execute(query, (login_usuario,))

            # Limpar o Treeview antes de inserir novos dados
            for item in tree.get_children():
                tree.delete(item)

            # Processar os resultados e adicionar ao Treeview
            resultados = cursor.fetchall()
            print(f"Resultados da consulta: {resultados}")  # Debug para verificar os dados retornados

            if not resultados:
                messagebox.showinfo("Sem Dados", "Nenhum curso encontrado para este usuário.")
                return

            for row in resultados:
                identificador, titulo, carga_horaria, disponibilidade = row
                tree.insert("", "end", values=(identificador, titulo, carga_horaria, disponibilidade))

            # Fechar conexão
            cursor.close()
            conn.close()

        except Exception as e:
            messagebox.showerror("Erro ao Consultar", f"Não foi possível consultar os cursos inscritos.\n\n{e}")

    # Janela principal
    root = tk.Toplevel()
    root.title("Meus Cursos")
    root.geometry("700x400")
    root.resizable(False, False)

    # Configurando o frame superior para usar grid
    top_frame = tk.Frame(root, height=50)
    top_frame.pack(side="top", fill="x")

    # Configurar o grid dentro do `top_frame`
    top_frame.grid_columnconfigure(0, weight=1)  # Espaço antes do logo
    top_frame.grid_columnconfigure(2, weight=1)  # Espaço central
    top_frame.grid_columnconfigure(4, weight=1)  # Espaço após o botão

    # Substituir a imagem por um texto "CEUB"
    logo_label = tk.Label(top_frame, text="CEUB", font=("Helvetica", 16, "bold"), width=10, height=3, anchor="center")
    logo_label.grid(row=0, column=0, padx=10, sticky="w")  # Alinhado à esquerda

    # Campo de busca (no centro do grid)
    titulo = tk.Label(top_frame, text="Gestão de Cursos Monitoria", font='Helvetica 16 bold')
    titulo.grid(row=0, column=2, padx=20, sticky="ew")  # Expansível horizontalmente

    # Botão Nome do usuário (na direita do grid)
    botao_usuario = tk.Button(top_frame, text="Nome do usuário", font=("Arial", 12), command=lambda: abrir_dados_usuario(1))
    botao_usuario.grid(row=0, column=4, padx=20, sticky="e")  # Alinhado à direita

    # Barra lateral
    sidebar = tk.Frame(root, width=200)
    sidebar.pack(side="left", fill="y")

    # Botões do menu lateral
    btn_home = tk.Button(sidebar, text="home", font=("Arial", 10, "bold"), relief="flat")
    btn_home.pack(pady=10, padx=10, fill="x")

    # Linha que divide os botões
    separator = tk.Frame(sidebar, height=2, bg="white")
    separator.pack(fill="x", pady=10, padx=10)  # Adiciona margens laterais de 20px

    # Botão de meus cursos
    btn_meus_cursos = tk.Button(sidebar, text="Meus Cursos", font=("Arial", 10, "bold"), relief="flat", bg="lightblue", fg="White")
    btn_meus_cursos.pack(pady=10, padx=10, fill="x")

    # Botão de descobrir
    btn_descobrir = tk.Button(sidebar,text="Descobrir",font=("Arial", 10, "bold"),relief="flat")
    btn_descobrir.pack(pady=10, padx=10, fill="x")

    # Linha que divide os botões
    separator = tk.Frame(sidebar, height=2, bg="white")
    separator.pack(fill="x", pady=10, padx=10)  # Adiciona margens laterais de 20px

    # Área de conteúdo principal
    content_area = tk.Frame(root)
    content_area.pack(side="right", expand=True, fill="both")

    # ========================== Treeview na Área de Conteúdo ==========================

    def criar_treeview(parent):
        # Campo de consulta
        lb_nome = tk.Label(parent, text="Pesquise o seu curso:", font='Arial 12')
        lb_nome.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        nome_var = tk.StringVar()
        et_nome = ttk.Entry(parent, width=30, textvariable=nome_var, font='Arial 12')
        et_nome.grid(row=0, column=1, pady=10)

        bt_consultar = tk.Button(parent, text="Consultar", command=lambda: consultar_cursos_inscritos(tree, perfil))
        bt_consultar.grid(row=0, column=2, padx=10, pady=10)

        # Criar Treeview para exibir os cursos inscritos
        tree = ttk.Treeview(parent, columns=("Identificador", "Título", "Carga_horaria", "Disponivel"), show="headings")
        tree.heading("Identificador", text="Identificador")
        tree.heading("Título", text="Título")
        tree.heading("Carga_horaria", text="Carga Horária")
        tree.heading("Disponivel", text="Disponibilidade")
        tree.column("Identificador", width=80)
        tree.column("Título", width=300)
        tree.column("Carga_horaria", width=80)
        tree.column("Disponivel", width=100)
        tree.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

        # Botões de operação
        bt_abrir = tk.Button(parent, text="Abrir", command=lambda: abrir_curso(tree, perfil))
        bt_abrir.grid(row=2, column=2, padx=10, pady=10)

        bt_incluir = tk.Button(parent, text="Desinscrever", command=lambda: desinscrever_curso(tree, perfil))
        bt_incluir.grid(row=2, column=0, padx=10, pady=10)

        return tree



    # Adicionando o Treeview na área de conteúdo
    tree = criar_treeview(content_area)

    root.mainloop()