import tkinter as tk

class LoginUsuario:
    def __init__(self):

        # Configuração da janela principal
        self.janela = tk.Tk()
        self.janela.title('Login Usuário')
        self.janela.geometry('300x240')
        self.janela.resizable(False, False)

        # Label "Login"
        label_login = tk.Label(self.janela, text="LOGIN", font=("Arial", 10, "bold"))
        label_login.pack(pady=(10, 5))  # Espaçamento acima do campo
        self.term1 = tk.Entry(self.janela, width=25, justify="center", font=("Arial", 12))
        self.term1.pack(pady=(0, 15))  # Espaçamento abaixo do campo

        # Label "Senha"
        label_senha = tk.Label(self.janela, text="SENHA", font=("Arial", 10, "bold"))
        label_senha.pack(pady=(10, 5))  # Espaçamento acima do campo
        self.term2 = tk.Entry(self.janela, width=25, justify="center", font=("Arial", 12), show="*")
        self.term2.pack(pady=(0, 20))  # Espaçamento abaixo do campo

        # Frame para os botões
        button_frame = tk.Frame(self.janela)
        button_frame.pack(pady=(10, 0))  # Espaçamento acima do frame dos botões

        # Botão de Login
        btn_login = tk.Button(button_frame, text="Entrar", width=12, font=("Arial", 10, "bold"))
        btn_login.pack(side="left", padx=5)  # Espaçamento lateral

        # Botão de Registro
        btn_registro = tk.Button(button_frame, text="Registrar", width=12, font=("Arial", 10, "bold"))
        btn_registro.pack(side="left", padx=5)  # Espaçamento lateral

    def run(self):
        self.janela.mainloop()


if __name__ == "__main__":
    login = LoginUsuario()
    login.run()