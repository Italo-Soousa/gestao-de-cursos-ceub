import tkinter as tk
from tkinter import ttk, PhotoImage, messagebox
from util.db import conexaoBanco  # Certifique-se de ter a classe SQL configurada
from paginaDadosUsuario import abrir_dados_usuario


def consultar_dados(tree):
    try:
        # Conectar ao banco de dados
        conn = conexaoBanco()
        cursor = conn.cursor()

        # Executar a consulta SQL (adicionando o campo de vagas)
        cursor.execute("SELECT id, titulo, carga_horaria, vagas FROM Cursos")

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


# Janela principal
root = tk.Tk()
root.title("Gestão de Cursos")
root.geometry("800x450")
root.resizable(False, False)

# Configurando o frame superior para usar grid
top_frame = tk.Frame(root, height=50)
top_frame.pack(side="top", fill="x")

# Configurar o grid dentro do `top_frame`
top_frame.grid_columnconfigure(0, weight=1)  # Espaço antes do logo
top_frame.grid_columnconfigure(2, weight=1)  # Espaço central
top_frame.grid_columnconfigure(4, weight=1)  # Espaço após o botão

# Imagem CEUB (na parte esquerda do grid)
logo_img = PhotoImage(file="/Users/italosousa/Desktop/Projeto Faculdade/interface/imagens/uniceub.png")
logo_label = tk.Label(top_frame, image=logo_img)
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
btn_descobrir = tk.Button(sidebar, text="Descobrir", font=("Arial", 10, "bold"), relief="flat")
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
    tree = ttk.Treeview(parent, columns=("Identificador", "Título", "Dias", "Horario", "Data de Inicio"), show="headings")
    tree.heading("Identificador", text="Identificador")
    tree.heading("Título", text="Título")
    tree.heading("Dias", text="Frequência")
    tree.heading("Horario", text="Horário")
    tree.heading("Data de Inicio", text="Data de Início")
    tree.column("Identificador", width=80)
    tree.column("Título", width=300)
    tree.column("Dias", width=80)
    tree.column("Horario", width=100)
    tree.column("Data de Inicio", width=100)
    tree.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

    # Botões de operação
    bt_incluir = tk.Button(parent, text="Abrir", command=lambda: InscreverCurso())
    bt_incluir.grid(row=2, column=0, padx=10, pady=10)

    bt_incluir = tk.Button(parent, text="Desinscrever", command=lambda: InscreverCurso())
    bt_incluir.grid(row=2, column=2, padx=10, pady=10)

    return tree


# Adicionando o Treeview na área de conteúdo
tree = criar_treeview(content_area)

root.mainloop()