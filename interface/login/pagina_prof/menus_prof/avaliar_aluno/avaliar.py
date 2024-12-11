import tkinter as tk
from util.db import conexaoBanco
from tkinter import messagebox
from util.config import cor0, config_botao, config_text_box, config_text


def avaliar(id_aluno, id_curso, nome):
    JDA = tk.Tk()
    JDA.title("Janela de Avaliação")
    JDA.geometry("600x230")
    JDA.configure(bg=cor0)
    JDA.resizable(False, False)
    nota_entry = tk.Entry(JDA, **config_text_box, width=20)
    nota_entry.place(x=20, y=80)
    presenca_entry = tk.Entry(JDA, **config_text_box, width=20)
    presenca_entry.place(x=20, y=140)
    try:
        # Conecta ao banco usando o util.db
        conexao = conexaoBanco()
        if conexao:
            cursor = conexao.cursor()

            # Consulta as informações do curso pelo login
            cursor.execute(
                "SELECT nota_aluno, presenca_aluno,id_inscricao FROM inscricoes WHERE id_curso = %s AND id_perfis = %s",
                (id_curso, id_aluno))
            resultado = cursor.fetchone()

            if resultado:
                nota_aluno, presenca_aluno, id_inscricao = resultado
                print(resultado)
                # Exibindo o título com o login do curso
                texto_informativo = tk.Label(JDA, text=f"Nome Do Aluno: {nome}", **config_text)
                texto_informativo.place(x=20, y=20)

                # senha
                texto_senha = tk.Label(JDA, text=f"Nota do Aluno: {nota_aluno}", **config_text)
                texto_senha.place(x=20, y=50)

                texto_email = tk.Label(JDA, text=f"Presença do Aluno: {presenca_aluno}", **config_text)
                texto_email.place(x=20, y=110)

            cursor.close()
            conexao.close()
        else:
            print("Erro", "Não foi possível conectar ao banco de dados.")
    except Exception as e:
        print("Erro", f"Ocorreu um erro ao salvar: {e}")

    def salvarDados():

        nota_aluno = nota_entry.get()
        presenca_aluno = presenca_entry.get()

        # Verificando se os dados não estão vazios
        if not nota_aluno and not presenca_aluno:
            messagebox.showwarning("Aviso", "Nenhum campo foi preenchido para atualização.")
            return

        try:
            # Conecta ao banco usando o util.db
            conexao = conexaoBanco()
            if conexao:
                cursor = conexao.cursor()

                update_values = []
                update_query = "UPDATE inscricoes SET "
                if nota_aluno:
                    update_query += "nota_aluno = %s, "
                    update_values.append(nota_aluno)
                if presenca_aluno:
                    update_query += "presenca_aluno = %s, "
                    update_values.append(presenca_aluno)

                # Remove a vírgula final, caso algum campo não tenha sido alterado
                if update_values:
                    update_query = update_query.rstrip(", ")  # Remove a vírgula extra no final
                    update_query += " WHERE id_inscricao = %s"
                    update_values.append(id_inscricao)
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

                JDA.destroy()
            else:
                messagebox.showerror("Erro", "Não foi possível conectar ao banco de dados.")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao salvar: {e}")

    # Botão para registrar
    bntDeRegistro = tk.Button(JDA, text="Confirmar", **config_botao, width=12, command=salvarDados)
    bntDeRegistro.place(x=475, y=180)
    JDA.mainloop()
