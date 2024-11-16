import tkinter as tk


class LoginUsuario:
    def __init__(self):

        # Configurar a janela principal
        self.janela = tk.Tk()
        self.janela.title('Login Usuário')
        self.janela.geometry("300x350")
        self.janela.resizable(False, False)

        # Círculo no topo
        self.canvas = tk.Canvas(self.janela, width=80, height=80, highlightthickness=0)
        self.canvas.create_oval(10, 10, 70, 70, fill="#6d6d6d", outline="")  # Cor cinza para o círculo
        self.canvas.pack(pady=(30, 10))  # Espaçamento no topo

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

        # Botão de Login
        btn_login = tk.Button(self.janela, text="Entrar", width=15, font=("Arial", 10, "bold"))
        btn_login.pack(pady=(10, 0))  # Espaçamento abaixo do botão

    def run(self):
        self.janela.mainloop()


if __name__ == "__main__":
    login = LoginUsuario()
    login.run()