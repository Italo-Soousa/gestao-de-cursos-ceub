import tkinter as tk
from tkinter import ttk

def abrir_pagina_curso(curso_id, detalhes_curso):

    nova_janela = tk.Toplevel()  # Cria uma janela
    nova_janela.title(f"Gestão de Cursos UNI-CEUB")
    nova_janela.geometry("600x400")
    nova_janela.configure(bg="#333333")  # Fundo escuro para combinar com o tema da imagem

    # Título do curso
    titulo_label = tk.Label(nova_janela, text=detalhes_curso['nome'], font='Helvetica 20 bold', fg="white", bg="#333333")
    titulo_label.pack(pady=20)

    # Campos detalhados
    frame_detalhes = tk.Frame(nova_janela, bg="#333333")
    frame_detalhes.pack(pady=10)

    # Campo Carga Horária
    tk.Label(frame_detalhes, text="Carga horária:", font="Arial 14", fg="white", bg="#333333").grid(row=0, column=0, sticky="w", padx=20, pady=5)
    tk.Label(frame_detalhes, text=f"{detalhes_curso['carga_horaria']} horas", font="Arial 14", fg="white", bg="#333333").grid(row=0, column=1, sticky="w", padx=10)

    # Campo Vagas
    tk.Label(frame_detalhes, text="Vagas:", font="Arial 14", fg="white", bg="#333333").grid(row=1, column=0, sticky="w", padx=20, pady=5)
    tk.Label(frame_detalhes, text=f"{detalhes_curso['vagas']}", font="Arial 14", fg="white", bg="#333333").grid(row=1, column=1, sticky="w", padx=10)

    # Campo Disponibilidade
    tk.Label(frame_detalhes, text="Disponibilidade:", font="Arial 14", fg="white", bg="#333333").grid(row=1, column=2, sticky="w", padx=20, pady=5)
    tk.Label(frame_detalhes, text=f"{detalhes_curso['disponibilidade']}", font="Arial 14", fg="white", bg="#333333").grid(row=1, column=3, sticky="w", padx=10)

    # Campo Descrição
    tk.Label(frame_detalhes, text="Descrição:", font="Arial 14", fg="white", bg="#333333").grid(row=2, column=0, sticky="w", padx=20, pady=5)
    descricao_label = tk.Label(frame_detalhes, text=f"{detalhes_curso['descricao']}", font="Arial 14", fg="white", bg="#333333", wraplength=500, justify="left")
    descricao_label.grid(row=2, column=1, columnspan=3, sticky="w", padx=10)

    # Botão Fechar
    tk.Button(nova_janela, text="Fechar", command=nova_janela.destroy, bg="#555555", fg="white", font="Arial 12").pack(pady=20)