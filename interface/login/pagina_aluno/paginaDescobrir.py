import tkinter as tk
from tkinter import ttk, PhotoImage, messagebox
from util.db import conexaoBanco
from paginaDadosUsuario import abrir_dados_usuario
from paginaCurso import abrir_pagina_curso
from paginaMeusCursos import abrir_pagina_meus_cursos
from Compartilhado import inscricoes
import os

def inscrever_curso(tree, id_perfis):
    """
    Inscreve o curso selecionado no banco de dados para o usuário logado.
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
            "SELECT * FROM inscricoes WHERE id_perfis = %s AND id_curso = %s",
            (id_perfis, curso_id)
        )
        if cursor.fetchone():
            messagebox.showinfo("Curso já Inscrito", "Você já está inscrito nesse curso.")
            conn.close()
            return

        # Inserir a inscrição na tabela `inscricoes`
        cursor.execute(
            "INSERT INTO inscricoes (id_perfis, id_curso) VALUES (%s, %s)",
            (id_perfis, curso_id)
        )
        conn.commit()  # Confirmar a transação

        # Mensagem de sucesso
        messagebox.showinfo("Inscrição Realizada", f"Você se inscreveu no curso: {titulo}")

        # Fechar conexão
        cursor.close()
        conn.close()

    except Exception as e:
        messagebox.showerror("Erro ao Inscrever", f"Ocorreu um erro ao se inscrever no curso.\n\n{e}")

def abrir_curso_selecionado(tree):
    try:
        # Obter o item selecionado no Treeview
        item_selecionado = tree.selection()

        if not item_selecionado:
            messagebox.showwarning("Nenhum Curso Selecionado", "Por favor, selecione um curso para abrir.")
            return

        # Extrair os valores da linha selecionada
        valores = tree.item(item_selecionado, 'values')
        curso_id = valores[0]  # Supondo que o ID está na primeira coluna

        # Verificar se o ID é válido
        if not curso_id:
            messagebox.showerror("Erro", "Não foi possível obter o ID do curso.")
            return

        # Chamar a função para abrir a nova página
        abrir_pagina_curso(curso_id)  # Função importada de outro arquivo

    except Exception as e:
        messagebox.showerror("Erro ao Abrir Curso", f"Ocorreu um erro ao tentar abrir o curso.\n\n{e}")

def consultar_dados(tree):
    try:
        # Conectar ao banco de dados
        conn = conexaoBanco()
        cursor = conn.cursor()

        # Executar a consulta SQL (adicionando o campo de vagas)
        cursor.execute("SELECT id_curso, nome, carga_horaria, vagas FROM curso")

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

def buscar_detalhes_curso(curso_id):
    """
    Busca os detalhes do curso no banco de dados com base no ID.

    Args:
        curso_id (str): ID do curso a ser buscado.

    Returns:
        dict: Dicionário com os detalhes do curso.
    """
    try:
        conn = conexaoBanco()
        cursor = conn.cursor()

        # Consulta ao banco de dados
        cursor.execute("SELECT nome, carga_horaria, vagas, descricao FROM curso WHERE id_curso = %s", (curso_id,))
        resultado = cursor.fetchone()
        conn.close()

        if resultado:
            titulo, carga_horaria, vagas, descricao = resultado
            disponibilidade = "Disponível" if vagas > 0 else "Indisponível"

            return {
                'nome': titulo,
                'carga_horaria': carga_horaria,
                'vagas': vagas,
                'disponibilidade': disponibilidade,
                'descricao': descricao
            }
        else:
            messagebox.showerror("Erro", "Curso não encontrado.")
            return None

    except Exception as e:
        messagebox.showerror("Erro ao Buscar Curso", f"Erro ao buscar os detalhes do curso.\n\n{e}")
        return None

def abrir_curso(tree):
    """
    Coleta o ID do curso selecionado e abre a página de detalhes do curso.
    """
    item_selecionado = tree.selection()

    if not item_selecionado:
        messagebox.showwarning("Nenhum Curso Selecionado", "Por favor, selecione um curso para abrir.")
        return

    valores = tree.item(item_selecionado, 'values')
    curso_id = valores[0]  # Supondo que o ID está na primeira coluna

    detalhes_curso = buscar_detalhes_curso(curso_id)
    if detalhes_curso:
        abrir_pagina_curso(curso_id, detalhes_curso)

# Janela principal
root = tk.Tk()
root.title("Gestão de Cursos")
root.geometry("700x400")
root.resizable(False, False)

# Configurando o frame superior para usar grid
top_frame = tk.Frame(root, height=50)
top_frame.pack(side="top", fill="x")

# Configurar o grid dentro do `top_frame`
top_frame.grid_columnconfigure(0, weight=1)  # Espaço antes do logo
top_frame.grid_columnconfigure(2, weight=1)  # Espaço central
top_frame.grid_columnconfigure(4, weight=1)  # Espaço após o botão

# Imagem CEUB (na parte esquerda do grid)
diretorio_atual = os.path.dirname(__file__)
caminho_imagem = os.path.join(diretorio_atual, "..", "..", "imagens", "uniceub.png")
logo_img = PhotoImage(file=caminho_imagem)
logo_label = tk.Label(top_frame, image=logo_img)
logo_label.grid(row=0, column=0, padx=10, sticky="w")  # Alinhado à esquerda

# Campo de busca (no centro do grid)
titulo = tk.Label(top_frame, text="Gestão de Cursos Monitoria", font='Helvetica 16 bold')
titulo.grid(row=0, column=2, padx=20, sticky="ew")  # Expansível horizontalmente

# Botão Nome do usuário (na direita do grid)
botao_usuario = tk.Button(top_frame, text="Nome do usuário", font=("Arial", 12), command=lambda: abrir_dados_usuario(3))
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

# Adicionar botão na barra lateral para abrir Meus Cursos
btn_meus_cursos = tk.Button(sidebar, text="Meus Cursos", font=("Arial", 10, "bold"), relief="flat", command=lambda: abrir_pagina_meus_cursos())
btn_meus_cursos.pack(pady=10, padx=10, fill="x")

# Botão de descobrir
btn_descobrir = tk.Button(sidebar, text="Descobrir", font=("Arial", 10, "bold"), relief="flat", bg="lightblue", fg="White")
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

    bt_consultar = tk.Button(parent, text="Consultar", command=lambda: consultar_dados(tree))
    bt_consultar.grid(row=0, column=2, padx=10, pady=10)

    # Treeview para exibir os resultados
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
    bbt_incluir = tk.Button(content_area, text="Inscrever", command=lambda: inscrever_curso(tree, id_perfis=1))
    bbt_incluir.grid(row=2, column=0, padx=10, pady=10)

    bt_abrir = tk.Button(parent, text="Abrir", command=lambda: abrir_curso(tree))
    bt_abrir.grid(row=2, column=2, padx=10, pady=10)

    return tree


# Adicionando o Treeview na área de conteúdo
tree = criar_treeview(content_area)

root.mainloop()