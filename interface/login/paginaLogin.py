import tkinter as tk
from tkinter import messagebox, simpledialog
from interface.login.pagina_adm import menu_adm
from paginaRegistro import abrirPaginaRegistro
from util.db import conexaoBanco  # Importa a função de conexão
def LoginUsuario():
    # Função para validar a senha antes de acessar a página de registro
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

    def abrirPaginaAluno():
        aluno_window = tk.Tk()
        aluno_window.title("Página do Aluno")
        tk.Label(aluno_window, text="Bem-vindo à página do Aluno!").pack()
        aluno_window.mainloop()

    def loginUsuario():
        usuario = term1.get()
        senha = term2.get()

        # Conectar ao banco de dados
        conexao = conexaoBanco()
        cursor = conexao.cursor()

        try:
            # Consulta SQL para validar login e obter tipo de usuário
            cursor.execute(
                "SELECT tipo_usuario FROM perfis WHERE login = %s AND senha = %s",
                (usuario, senha)
            )
            resultado = cursor.fetchone()  # Retorna a primeira linha encontrada

            if resultado:
                tipo_usuario = resultado[0]  # Pega o valor de 'tipo_usuario'
                messagebox.showinfo("Login Bem-Sucedido", f"Bem-vindo, {usuario}!")

                # Fecha a janela de login
                janela.destroy()

                # Redireciona com base no tipo de usuário
                if tipo_usuario == "administrador":
                    menu_adm.iniciar(usuario)
                elif tipo_usuario == "aluno":
                    abrirPaginaAluno()
                else:
                    messagebox.showerror("Erro", "Tipo de usuário desconhecido.")
            else:
                messagebox.showerror("Erro de Login", "Usuário ou senha incorretos. Tente novamente.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao conectar ao banco: {e}")
        finally:
            # Fechar conexão com o banco
            cursor.close()
            conexao.close()

    # Frame para os botões
    button_frame = tk.Frame(janela)
    button_frame.pack(pady=(10, 0))  # Espaçamento acima do frame dos botões

    # Botão de Login
    btn_login = tk.Button(button_frame, text="Entrar", width=12, font=("Arial", 10, "bold"), command=loginUsuario)
    btn_login.pack(side="left", padx=5)  # Espaçamento lateral

    # Botão de Registro com validação de senha
    btn_registro = tk.Button(button_frame, text="Registrar", width=12, font=("Arial", 10, "bold"), command=solicitarSenha)
    btn_registro.pack(side="left", padx=5)  # Espaçamento lateral

    # Executar o loop principal da janela
    janela.mainloop()

# Chamar a função LoginUsuario para iniciar o programa
if __name__ == "__main__":
    LoginUsuario()