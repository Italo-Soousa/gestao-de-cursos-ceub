import tkinter as tk
from tkinter import messagebox
from util.db import conexaoBanco

def abrir_dados_usuario(perfil):

    # Criar a janela principal
    janela_usuario = tk.Toplevel()
    janela_usuario.title("Seus Dados")
    janela_usuario.geometry("400x300")
    janela_usuario.resizable(False, False)

    try:
        # Conectar ao banco de dados
        conexao = conexaoBanco()
        cursor = conexao.cursor()

        # Consultar os dados do usuário
        cursor.execute("SELECT nome, email, login, senha, tipo_usuario FROM perfis WHERE login = %s", (perfil,))
        resultado = cursor.fetchone()

        if resultado:
            nome, email, login, senha, tipo_usuario = resultado

            # Exibir os dados do usuário
            tk.Label(janela_usuario, text="Seus Dados", font=("Arial", 16, "bold")).pack(pady=10)

            tk.Label(janela_usuario, text=f"Nome: {nome}", font=("Arial", 12)).pack(anchor="w", padx=20, pady=5)
            tk.Label(janela_usuario, text=f"Email: {email}", font=("Arial", 12)).pack(anchor="w", padx=20, pady=5)
            tk.Label(janela_usuario, text=f"Login: {login}", font=("Arial", 12)).pack(anchor="w", padx=20, pady=5)
            tk.Label(janela_usuario, text=f"Senha: {senha}", font=("Arial", 12)).pack(anchor="w", padx=20, pady=5)
            tk.Label(janela_usuario, text=f"Tipo de Usuário: {tipo_usuario}", font=("Arial", 12)).pack(anchor="w", padx=20, pady=5)
        else:
            messagebox.showerror("Erro", "Usuário não encontrado!")
            janela_usuario.destroy()

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao conectar ao banco de dados: {e}")
        janela_usuario.destroy()
    finally:
        if 'conexao' in locals() and conexao.is_connected():
            cursor.close()
            conexao.close()