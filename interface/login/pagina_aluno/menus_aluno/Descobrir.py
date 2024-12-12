import tkinter as tk
from tkinter import ttk, messagebox
from util.db import conexaoBanco
from interface.login.pagina_aluno.menus_aluno.MeusCursos import meusCursos
from interface.login.pagina_aluno.menus_aluno.DadosUsuario import abrir_dados_usuario
from interface.login.pagina_aluno.menus_aluno.PaginaCurso import abrir_pagina_curso

def descobrir(perfil):

    def abrir_curso(tree, perfil):
        """
        Abre os detalhes do curso selecionado no Treeview e permite a inscrição.
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

            # Extrair as informações do curso
            identificador, titulo_curso, carga_horaria, disponibilidade = valores

            # Obter a descrição do curso no banco de dados
            try:
                conn = conexaoBanco()
                cursor = conn.cursor()

                # Consulta para obter a descrição do curso
                cursor.execute("""
                    SELECT descricao FROM cursos WHERE id_curso = %s
                """, (identificador,))
                resultado = cursor.fetchone()
                descricao = resultado[0] if resultado else "Descrição não disponível."

                cursor.close()
                conn.close()
            except Exception as e:
                descricao = "Erro ao carregar descrição."
                print(f"Erro ao obter a descrição do curso: {e}")

            # Criar uma nova janela para exibir os detalhes do curso
            detalhes_janela = tk.Toplevel()
            detalhes_janela.title(f"Detalhes do Curso: {titulo_curso}")
            detalhes_janela.geometry("400x400")

            # Exibir os detalhes do curso
            tk.Label(detalhes_janela, text="Detalhes do Curso", font=("Arial", 16, "bold")).pack(pady=10)
            tk.Label(detalhes_janela, text=f"Identificador: {identificador}", font=("Arial", 12)).pack(pady=5)
            tk.Label(detalhes_janela, text=f"Título: {titulo_curso}", font=("Arial", 12)).pack(pady=5)
            tk.Label(detalhes_janela, text=f"Carga Horária: {carga_horaria} horas", font=("Arial", 12)).pack(pady=5)
            tk.Label(detalhes_janela, text=f"Disponibilidade: {disponibilidade}", font=("Arial", 12)).pack(pady=5)
            tk.Label(detalhes_janela, text="Descrição:", font=("Arial", 12, "bold")).pack(pady=5)
            tk.Label(detalhes_janela, text=descricao, font=("Arial", 12), wraplength=350, justify="left").pack(pady=5)

            # Botão para fechar a janela de detalhes
            tk.Button(detalhes_janela, text="Fechar", command=detalhes_janela.destroy).pack(pady=10)

        except Exception as e:
            messagebox.showerror("Erro ao Abrir Curso", f"Ocorreu um erro ao tentar abrir os detalhes do curso.\n\n{e}")

    def consultar_dados(tree):
        try:
            # Conectar ao banco de dados
            conn = conexaoBanco()
            cursor = conn.cursor()

            # Executar a consulta SQL (adicionando o campo de vagas)
            cursor.execute("SELECT id_curso, nome, carga_horaria, vagas FROM cursos")

            # Limpar o Treeview antes de inserir novos dados
            for item in tree.get_children():
                tree.delete(item)

            # Processar os resultados e adicionar ao Treeview
            for row in cursor.fetchall():
                id, titulo, carga_horaria, vagas = row
                disponibilidade = "Disponível" if vagas > 0 else "Indisponível"
                tree.insert("", "end", values=(id, titulo, carga_horaria, disponibilidade))

            # Fechar a conexão
            conn.close()

        except Exception as e:
            messagebox.showerror("Erro ao Consultar", f"Não foi possível consultar os dados.\n\n{e}")

    def inscrever_curso(tree, login_usuario):
        """
        Inscreve o curso selecionado no banco de dados usando o login do usuário.
        """
        try:
            # Obter o item selecionado
            item_selecionado = tree.selection()

            if not item_selecionado:
                messagebox.showwarning("Nenhum Curso Selecionado", "Por favor, selecione um curso para se inscrever.")
                return

            # Extrair os valores do curso selecionado
            valores = tree.item(item_selecionado, 'values')
            curso_id, titulo, carga_horaria, disponibilidade = valores

            # Conectar ao banco de dados
            conn = conexaoBanco()
            cursor = conn.cursor()

            # Verificar se o usuário já está inscrito no curso
            cursor.execute(
                """
                SELECT * FROM inscricoes i
                JOIN perfis p ON i.id_perfis = p.id_perfis
                WHERE p.login = %s AND i.id_curso = %s
                """,
                (login_usuario, curso_id)
            )
            if cursor.fetchone():
                messagebox.showinfo("Curso já Inscrito", "Você já está inscrito nesse curso.")
                conn.close()
                return

            # Inserir a inscrição na tabela `inscricoes`
            cursor.execute(
                """
                INSERT INTO inscricoes (id_perfis, id_curso, data_inscricao)
                SELECT p.id_perfis, %s, NOW()
                FROM perfis p
                WHERE p.login = %s
                """,
                (curso_id, login_usuario)
            )
            conn.commit()  # Confirmar a transação

            # Mensagem de sucesso
            messagebox.showinfo("Inscrição Realizada", f"Você se inscreveu no curso: {titulo}")

            # Fechar conexão
            cursor.close()
            conn.close()

        except Exception as e:
            messagebox.showerror("Erro ao Inscrever", f"Ocorreu um erro ao se inscrever no curso.\n\n{e}")

    """
    Função para abrir a página Descobrir.
    """
    # Janela principal
    root = tk.Tk()
    root.title("Descobrir")
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
    botao_usuario = tk.Button(top_frame, text="Meu Perfil", font=("Arial", 12), command=lambda: abrir_dados_usuario(perfil))
    botao_usuario.grid(row=0, column=4, padx=20, sticky="e")  # Alinhado à direita

    # Barra lateral
    sidebar = tk.Frame(root, width=200)
    sidebar.pack(side="left", fill="y")

    # Botões do menu lateral
    btn_home = tk.Button(sidebar, text="home", font=("Arial", 10, "bold"), relief="flat")
    btn_home.pack(pady=10, padx=10, fill="x")

    separator = tk.Frame(sidebar, height=2, bg="white")
    separator.pack(fill="x", pady=10, padx=10)  # Linha separadora

    btn_meus_cursos = tk.Button(sidebar, text="Meus Cursos", font=("Arial", 10, "bold"), relief="flat", command=lambda: meusCursos(perfil))
    btn_meus_cursos.pack(pady=10, padx=10, fill="x")

    btn_descobrir = tk.Button(sidebar, text="Descobrir", font=("Arial", 10, "bold"), relief="flat", bg="lightblue", fg="White")
    btn_descobrir.pack(pady=10, padx=10, fill="x")

    separator = tk.Frame(sidebar, height=2, bg="white")
    separator.pack(fill="x", pady=10, padx=10)  # Linha separadora

    # Área de conteúdo principal
    content_area = tk.Frame(root)
    content_area.pack(side="right", expand=True, fill="both")

    # ========================== Treeview na Área de Conteúdo ==========================
    def criar_treeview(parent):
        lb_nome = tk.Label(parent, text="Pesquise o seu curso:", font='Arial 12')
        lb_nome.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        nome_var = tk.StringVar()
        et_nome = ttk.Entry(parent, width=30, textvariable=nome_var, font='Arial 12')
        et_nome.grid(row=0, column=1, pady=10)

        bt_consultar = tk.Button(parent, text="Consultar", command=lambda: consultar_dados(tree))
        bt_consultar.grid(row=0, column=2, padx=10, pady=10)

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

        bbt_incluir = tk.Button(content_area, text="Inscrever-se", command=lambda: inscrever_curso(tree, perfil))
        bbt_incluir.grid(row=2, column=0, padx=10, pady=10)

        bt_abrir = tk.Button(parent, text="Abrir", command=lambda: abrir_curso(tree, perfil))
        bt_abrir.grid(row=2, column=2, padx=10, pady=10)

        return tree

    tree = criar_treeview(content_area)

    root.mainloop()