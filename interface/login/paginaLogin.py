import tkinter as tk
from tkinter import messagebox, simpledialog
from paginaRegistro import abrirPaginaRegistro

def LoginUsuario():
    # Função para validar a senha antes de acessar a página de registro registro
    def solicitarSenha():
        senha_admin = simpledialog.askstring(
            "Senha Requerida", "Digite a senha de administrador para continuar:", show="*"
        )
        if senha_admin == "123":  # Substitua "123" pela sua senha desejada
            messagebox.showinfo("Acesso Permitido", "Senha correta! Acessando registro.")
            abrirPaginaRegistro()  # Chama a página de registro
        else:
            messagebox.showerror("Acesso Negado", "Senha incorreta. Tente novamente.")

    # Configuração da janela principal
    janela = tk.Tk()
    janela.title('Login Usuário')
    janela.geometry('300x240')
    janela.resizable(False, False)

    # Label "Login"
    label_login = tk.Label(janela, text="LOGIN", font=("Arial", 10, "bold"))
    label_login.pack(pady=(10, 5))  # Espaçamento acima do campo
    term1 = tk.Entry(janela, width=25, justify="center", font=("Arial", 12))
    term1.pack(pady=(0, 15))  # Espaçamento abaixo do campo

    # Label "Senha"
    label_senha = tk.Label(janela, text="SENHA", font=("Arial", 10, "bold"))
    label_senha.pack(pady=(10, 5))  # Espaçamento acima do campo
    term2 = tk.Entry(janela, width=25, justify="center", font=("Arial", 12), show="*")
    term2.pack(pady=(0, 20))  # Espaçamento abaixo do campo

    # Frame para os botões (espaço na janela para os botões ficarem um do lado do outro)
    button_frame = tk.Frame(janela)
    button_frame.pack(pady=(10, 0))  # Espaçamento acima do frame dos botões

    # Botão de Login
    btn_login = tk.Button(button_frame, text="Entrar", width=12, font=("Arial", 10, "bold"))
    btn_login.pack(side="left", padx=5)  # Espaçamento lateral

    # Botão de Registro com validação de senha
    btn_registro = tk.Button(button_frame, text="Registrar", width=12, font=("Arial", 10, "bold"), command=solicitarSenha)
    btn_registro.pack(side="left", padx=5)  # Espaçamento lateral

    # Executar o loop principal da janela
    janela.mainloop()

# Chamar a função LoginUsuario para iniciar o programa
if __name__ == "__main__":
    LoginUsuario()