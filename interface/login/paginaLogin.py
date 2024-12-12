import tkinter as tk
from tkinter import messagebox, simpledialog, PhotoImage
from interface.login.pagina_adm import menu_adm
from interface.login.pagina_aluno import menu_home
from paginaRegistro import abrirPaginaRegistro
from util.db import conexaoBanco  # Importa a função de conexão
from util.config import cor0, config_botao, config_text1, config_text_box
import os

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
    janela.geometry('280x300')
    janela.configure(bg=cor0)
    janela.resizable(False, False)

    # Imagem CEUB
    diretorio_atual = os.path.dirname(__file__)
    caminho_imagem = os.path.join(diretorio_atual, "..", "imagens", "uniceub.png")
    logo_img = PhotoImage(file=caminho_imagem)

    logo_label = tk.Label(janela, image=logo_img, bd=0, relief="solid")
    logo_label.place(x=95, y=0)

    # Label "Login"
    label_login = tk.Label(janela, text="LOGIN",**config_text1)
    label_login.place(x=105, y=70)  # Posiciona a label "LOGIN"
    term1 = tk.Entry(janela, width=25,**config_text_box)
    term1.place(x=25, y=105)  # Posiciona o campo de entrada do login

    # Label "Senha"
    label_senha = tk.Label(janela, text="SENHA",**config_text1)
    label_senha.place(x=105, y=145)  # Posiciona a label "SENHA"
    term2 = tk.Entry(janela, width=25,**config_text_box)
    term2.place(x=25, y=180)  # Posiciona o campo de entrada da senha


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
                    menu_home.iniciar(usuario)
                elif tipo_usuario == "professor":
                    from interface.login.pagina_prof import menu_prof
                    menu_prof.iniciar(usuario)
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

    # Botões
    btn_login = tk.Button(janela, text="Entrar",**config_botao, command=loginUsuario)
    btn_login.place(x=15, y=240)  # Posiciona o botão de login

    # Botão de Registro com validação de senha
    btn_registro = tk.Button(janela, text="Registrar",**config_botao, command=solicitarSenha)
    btn_registro.place(x=160, y=240)  # Posiciona o botão de registro

    # Executar o loop principal da janela
    janela.mainloop()

# Chamar a função LoginUsuario para iniciar o programa
if __name__ == "__main__":
    LoginUsuario()
