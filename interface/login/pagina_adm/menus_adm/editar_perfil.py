import tkinter as tk
from util.db import conexaoBanco
from tkinter import messagebox
def Editar_perfil(cor0, texto, login,cor3):
    JGC = tk.Tk()
    JGC.title(f"{login}")
    JGC.geometry("600x220")
    JGC.configure(bg=cor0)
    JGC.resizable(False, False)

    config_text = {
        'font': ("Arial", 13, "bold"),
        'fg': texto,
        'bg': cor0
    }
    senha_entry = tk.Entry(JGC, font=("Arial", 13), width=20, bg=cor3, bd=0, highlightthickness=0)
    senha_entry.place(x=20, y=80)
    email_entry = tk.Entry(JGC, font=("Arial", 13), width=20, bg=cor3, bd=0, highlightthickness=0)
    email_entry.place(x=20, y=140)
    try:
        # Conecta ao banco usando o util.db
        conexao = conexaoBanco()
        if conexao:
            cursor = conexao.cursor()

            # Consulta as informações do curso pelo login
            cursor.execute("SELECT senha, email, nome FROM perfis WHERE login = %s", (login,))
            resultado = cursor.fetchone()

            if resultado:
                senha, email, nome = resultado
                print(resultado)
                # Exibindo o título com o login do curso
                texto_informativo = tk.Label(JGC, text=f"Nome: {nome}", **config_text)
                texto_informativo.place(x=20, y=20)

                # senha
                texto_senha = tk.Label(JGC, text=f"Senha: {senha}", **config_text)
                texto_senha.place(x=20, y=50)

                texto_email  = tk.Label(JGC, text=f"Email: {email}", **config_text)
                texto_email .place(x=20, y=110)

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
                    update_query = update_query.rstrip(", ")  # Remove a vírgula extra no final
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
                # Fecha a conexão e o cursor
                cursor.close()
                conexao.close()

                # Fecha a janela de registro
                JGC.destroy()
            else:
                messagebox.showerror("Erro", "Não foi possível conectar ao banco de dados.")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao salvar: {e}")
    # Botão para registrar
    bntDeRegistro = tk.Button(JGC,font= ("Arial", 10, "bold"),text="Editar",bg= "#363636",fg= texto,relief= "flat",activebackground=cor3,width= 12,command=salvarDados)
    bntDeRegistro.place(x=475, y=180)
    JGC.mainloop()
