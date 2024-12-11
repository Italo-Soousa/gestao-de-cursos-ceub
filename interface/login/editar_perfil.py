import tkinter as tk
from util.db import conexaoBanco
from tkinter import messagebox
from util.config import cor0, config_botao, config_text_box, config_text1


def Editar_perfil(login):
    JEP = tk.Tk()
    JEP.title("Editar Perfil")
    JEP.geometry("600x230")
    JEP.configure(bg=cor0)
    JEP.resizable(False, False)

    senha_entry = tk.Entry(JEP, **config_text_box, width=20)
    senha_entry.place(x=20, y=80)
    email_entry = tk.Entry(JEP, **config_text_box, width=20)
    email_entry.place(x=20, y=140)
    try:
        conexao = conexaoBanco()
        if conexao:
            cursor = conexao.cursor()

            cursor.execute("SELECT senha, email, nome FROM perfis WHERE login = %s", (login,))
            resultado = cursor.fetchone()

            if resultado:
                senha, email, nome = resultado

                texto_informativo = tk.Label(JEP, text=f"Nome do Usuário: {nome}", **config_text1)
                texto_informativo.place(x=20, y=20)

                texto_senha = tk.Label(JEP, text=f"Senha do Usuário: {senha}", **config_text1)
                texto_senha.place(x=20, y=50)

                texto_email = tk.Label(JEP, text=f"Email do Usuário: {email}", **config_text1)
                texto_email.place(x=20, y=110)

            cursor.close()
            conexao.close()
        else:
            print("Erro", "Não foi possível conectar ao banco de dados.")
    except Exception as e:
        print("Erro", f"Ocorreu um erro ao salvar: {e}")

    def salvarDados():

        senha = senha_entry.get()
        email = email_entry.get()

        # Verificando se os dados não estão vazios
        if not senha and not email:
            messagebox.showwarning("Aviso", "Nenhum campo foi preenchido para atualização.")
            return

        try:
            # Conecta ao banco usando o util.db
            conexao = conexaoBanco()
            if conexao:
                cursor = conexao.cursor()

                update_values = []
                update_query = "UPDATE perfis SET "
                if senha:
                    update_query += "senha = %s, "
                    update_values.append(senha)
                if email:
                    update_query += "email = %s, "
                    update_values.append(email)

                # Remove a vírgula final, caso algum campo não tenha sido alterado
                if update_values:
                    update_query = update_query.rstrip(", ")
                    update_query += " WHERE login = %s"
                    update_values.append(login)
                    # Exibindo a consulta para debug
                    print(f"Consulta gerada: {update_query}")
                    print(f"Valores passados: {update_values}")
                    # Executando a consulta no banco
                    cursor.execute(update_query, tuple(update_values))
                    conexao.commit()
                    messagebox.showinfo("Sucesso", "Registro salvo com sucesso!")
                else:
                    messagebox.showwarning("Aviso", "Nenhum campo foi alterado.")

                cursor.close()
                conexao.close()

                JEP.destroy()
            else:
                messagebox.showerror("Erro", "Não foi possível conectar ao banco de dados.")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao salvar: {e}")

    # Botão para registrar
    bntDeRegistro = tk.Button(JEP, text="Editar", **config_botao, command=salvarDados)
    bntDeRegistro.place(x=475, y=180)
    JEP.mainloop()
