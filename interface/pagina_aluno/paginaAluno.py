import tkinter as tk
from tkinter import PhotoImage
from interface.pagina_aluno.paginaDadosUsuario import abrir_dados_usuario

# Configurações de cores e fontes
bg_color = "#D3D3D3"  # Cor de fundo geral
sidebar_color = "#F0F0F0"  # Cor do menu lateral
input_color = "#E8E8E8"  # Cor dos campos de entrada
button_color = "#A9A9A9"  # Cor dos botões
text_color = "#000000"  # Cor do texto

# Janela principal
root = tk.Tk()
root.title("Gestão de Cursos")
root.geometry("800x450")
root.configure(bg=bg_color)

# Configurando o frame superior para usar grid
top_frame = tk.Frame(root, bg=bg_color, height=50)
top_frame.pack(side="top", fill="x")

# Configurar o grid dentro do `top_frame`
top_frame.grid_columnconfigure(0, weight=1)  # Espaço antes do logo
top_frame.grid_columnconfigure(2, weight=1)  # Espaço central
top_frame.grid_columnconfigure(4, weight=1)  # Espaço após o botão

# Imagem CEUB ( na parte esquerda do grid )
logo_img = PhotoImage(file="/Users/italosousa/Desktop/Projeto Faculdade/interface/imagens/uniceub.png")
logo_label = tk.Label(top_frame, image=logo_img, bg=bg_color)
logo_label.grid(row=0, column=0, padx=10, sticky="w")  # Alinhado à esquerda

# Campo de busca ( no centro do grid )
search_entry = tk.Entry(top_frame, width=40, font=("Arial", 12), bg=input_color, fg=text_color)
search_entry.insert(0, "Qual curso você procura?")
search_entry.grid(row=0, column=2, padx=20, sticky="ew")  # Expansível horizontalmente

# Botão Nome do usuário ( na direita do grid )
botao_usuario = tk.Button(top_frame, text="Nome do usuário", font=("Arial", 12),bg="#E8E8E8",fg="#000000", command=lambda: abrir_dados_usuario(1))
botao_usuario.grid(row=0, column=4, padx=20, sticky="e")  # Alinhado à direita

# Barra lateral
sidebar = tk.Frame(root, bg=sidebar_color, width=200)
sidebar.pack(side="left", fill="y")

# Botões do menu lateral
btn_home = tk.Button(sidebar, text="home", bg=button_color, fg=text_color, font=("Arial", 10, "bold"), relief="flat")
btn_home.pack(pady=10, padx=10, fill="x")

# Linha que divide os botões
separator = tk.Frame(sidebar, height=2, bg=bg_color)
separator.pack(fill="x", pady=10, padx=10)  # Adiciona margens laterais de 20px

# Botão de meus cursos
btn_meus_cursos = tk.Button(sidebar, text="Meus Cursos", bg=button_color, fg=text_color, font=("Arial", 10, "bold"), relief="flat")
btn_meus_cursos.pack(pady=10, padx=10, fill="x")

# Botão de descobrir
btn_descobrir = tk.Button(sidebar, text="Descobrir", bg=button_color, fg=text_color, font=("Arial", 10, "bold"), relief="flat")
btn_descobrir.pack(pady=10, padx=10, fill="x")

# Linha que divide os botões
separator = tk.Frame(sidebar, height=2, bg=bg_color)
separator.pack(fill="x", pady=10, padx=10)  # Adiciona margens laterais de 20px

# Área de conteúdo principal
content_area = tk.Frame(root, bg="white")
content_area.pack(side="right", expand=True, fill="both")

root.mainloop()