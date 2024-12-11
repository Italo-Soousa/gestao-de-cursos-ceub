import tkinter as tk
from tkinter import ttk, PhotoImage, messagebox
from util.db import conexaoBanco
from paginaDadosUsuario import abrir_dados_usuario
from paginaMeusCursos import abrir_pagina_meus_cursos
import os

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
btn_home = tk.Button(sidebar, text="Home", font=("Arial", 10, "bold"), relief="flat")
btn_home.pack(pady=10, padx=10, fill="x")

separator = tk.Frame(sidebar, height=2, bg="white")
separator.pack(fill="x", pady=10, padx=10)  # Linha separadora

btn_meus_cursos = tk.Button(sidebar, text="Meus Cursos", font=("Arial", 10, "bold"), relief="flat", command=lambda: abrir_pagina_meus_cursos())
btn_meus_cursos.pack(pady=10, padx=10, fill="x")

btn_descobrir = tk.Button(sidebar, text="Descobrir", font=("Arial", 10, "bold"), relief="flat", bg="lightblue", fg="White")
btn_descobrir.pack(pady=10, padx=10, fill="x")

separator = tk.Frame(sidebar, height=2, bg="white")
separator.pack(fill="x", pady=10, padx=10)  # Linha separadora

# Área de conteúdo principal
content_area = tk.Frame(root)
content_area.pack(side="right", expand=True, fill="both")

# Mensagem de boas-vindas no topo da área de conteúdo
label_boas_vindas = tk.Label(content_area, text="Seja bem-vindo, João!", font="Arial 14", anchor="w", padx=10)
label_boas_vindas.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

def preencher_treeview(tree):
    """
    Preenche o Treeview com os cursos em que o usuário está inscrito.
    """
    try:
        conn = conexaoBanco()
        cursor = conn.cursor()

        # Consulta SQL para buscar os cursos do usuário
        cursor.execute("""
            SELECT 
                c.nome AS titulo, 
                i.nota_aluno, 
                i.presenca_aluno, 
                CASE 
                    WHEN i.nota_aluno >= 7 AND i.presenca_aluno >= 90 THEN 'Disponível'
                    ELSE 'Indisponível'
                END AS certificado
            FROM inscricoes i
            JOIN cursos c ON i.id_curso = c.id_curso
            WHERE i.id_perfis = %s
        """, (1,))  # Troque 1 pelo ID real do usuário logado

        # Preencher Treeview com os resultados da consulta
        for row in cursor.fetchall():
            tree.insert("", "end", values=row)

        cursor.close()
        conn.close()
    except Exception as e:
        messagebox.showerror("Erro ao carregar cursos", f"Erro: {e}")

def criar_treeview(parent):
    """
    Cria o Treeview e preenche automaticamente com os cursos do usuário.
    """
    tree = ttk.Treeview(parent, columns=("Título", "Nota", "Presença", "Certificado"), show="headings")
    tree.heading("Título", text="Título do Curso")
    tree.heading("Nota", text="Nota")
    tree.heading("Presença", text="Presença (%)")
    tree.heading("Certificado", text="Certificado")
    tree.column("Título", width=250)
    tree.column("Nota", width=80, anchor="center")
    tree.column("Presença", width=100, anchor="center")
    tree.column("Certificado", width=100, anchor="center")
    tree.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

    # Preencher automaticamente ao criar
    preencher_treeview(tree)

    return tree

# Adicionando o Treeview na área de conteúdo
tree = criar_treeview(content_area)

# Configuração da grade para content_area
content_area.grid_rowconfigure(1, weight=1)
content_area.grid_columnconfigure(0, weight=1)

root.mainloop()