import tkinter as tk
from tkinter import messagebox
from util.db import conexaoBanco  # Importa a função de conexão
from util.config import cor0, config_botao, config_text1, config_text_box

def abrirPaginaRegistro():



    # Cria uma nova janela para a página de registro
    pagina_registro = tk.Toplevel()
    pagina_registro.title("Página de Registro")
    pagina_registro.geometry("300x430")
    pagina_registro.configure(bg=cor0)
    pagina_registro.resizable(False, False)

    # Label "Nome"
    nome = tk.Label(pagina_registro, text="NOME",**config_text1)
    nome.pack(pady=(10, 5))
    PegandoNome = tk.Entry(pagina_registro, width=25,**config_text_box)
    PegandoNome.pack(pady=(0, 5))

    # Label "E-mail"
    email = tk.Label(pagina_registro, text="EMAIL",**config_text1)
    email.pack(pady=(10, 5))
    PegandoEmail = tk.Entry(pagina_registro, width=25,**config_text_box)
    PegandoEmail.pack(pady=(0, 5))

    # Label "Login"
    login = tk.Label(pagina_registro, text="LOGIN",**config_text1)
    login.pack(pady=(10, 5))
    PegandoLogin = tk.Entry(pagina_registro, width=25,**config_text_box)
    PegandoLogin.pack(pady=(0, 15))

    # Label "Senha"
    senha = tk.Label(pagina_registro, text="SENHA", **config_text1)
    senha.pack(pady=(10, 5))
    PegandoSenha = tk.Entry(pagina_registro, width=25,**config_text_box, show="*")
    PegandoSenha.pack(pady=(0, 20))

    # Label "Tipo de Usuário"
    senha = tk.Label(pagina_registro, text="TIPO USUÁRIO", **config_text1)
    senha.pack(pady=(10, 5))
    PaginaTipoUsuario = tk.Entry(pagina_registro, width=25,**config_text_box)
    PaginaTipoUsuario.pack(pady=(0, 20))

    # Função para salvar os dados no banco de dados
    def salvarDados():
        # Obtém os valores dos campos
        nome_valor = PegandoNome.get()
        email_valor = PegandoEmail.get()
        login_valor = PegandoLogin.get()
        senha_valor = PegandoSenha.get()
        tipoUsuario_valor = PaginaTipoUsuario.get()

        # Valida se todos os campos estão preenchidos
        if not nome_valor or not email_valor or not login_valor or not senha_valor:
            messagebox.showerror("Erro", "Todos os campos são obrigatórios!")
            return

        try:
            # Conecta ao banco usando o util.db
            conexao = conexaoBanco()
            if conexao:
                cursor = conexao.cursor()

                # Insere os dados na tabela "usuarios"
                cursor.execute("""
                    INSERT INTO perfis (nome, email, login, senha, tipo_usuario) 
                    VALUES (%s, %s, %s, %s, %s)
                """, (nome_valor, email_valor, login_valor, senha_valor, tipoUsuario_valor))

                # Confirma as alterações no banco
                conexao.commit()
                messagebox.showinfo("Sucesso", "Registro salvo com sucesso!")

                # Fecha a conexão e o cursor
                cursor.close()
                conexao.close()

                # Fecha a janela de registro
                pagina_registro.destroy()
            else:
                messagebox.showerror("Erro", "Não foi possível conectar ao banco de dados.")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao salvar: {e}")

    # Botão para registrar
    btn_registro = tk.Button(pagina_registro, text="Registrar", **config_botao, command=salvarDados)
    btn_registro.place(x=100, y=375)