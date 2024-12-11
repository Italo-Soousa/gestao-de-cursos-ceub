import tkinter as tk
from util.db import conexaoBanco
from tkinter import messagebox
from util.config import cor0, config_botao, config_text_box, config_text1


def Editar(nome):
    JEC = tk.Tk()
    JEC.title(f"Janela de Edição de Curso")
    JEC.geometry("600x310")
    JEC.configure(bg=cor0)
    JEC.resizable(False, False)
    vaga_entry = tk.Entry(JEC, **config_text_box, width=20)
    vaga_entry.place(x=20, y=80)
    carga_entry = tk.Entry(JEC, **config_text_box, width=20)
    carga_entry.place(x=20, y=140)
    descricao_entry = tk.Entry(JEC, **config_text_box, width=62)
    descricao_entry.place(x=20, y=230)
    try:
        conexao = conexaoBanco()
        if conexao:
            cursor = conexao.cursor()

            cursor.execute("SELECT vagas, carga_horaria, descricao FROM curso WHERE nome = %s", (nome,))
            resultado = cursor.fetchone()

            if resultado:
                vag, carga_horaria, desc = resultado

                texto_informativo = tk.Label(JEC, text=f"Nome Do Curso: {nome}", **config_text1)
                texto_informativo.place(x=20, y=20)

                texto_vagas = tk.Label(JEC, text=f"Vagas Do Curso: {vag}", **config_text1)
                texto_vagas.place(x=20, y=50)

                texto_carga = tk.Label(JEC, text=f"Carga Horaria Do Curso: {carga_horaria}", **config_text1)
                texto_carga.place(x=20, y=110)

                texto_descricao = tk.Label(JEC, text="Descrição Do Curso:", **config_text1)
                texto_descricao.place(x=200, y=170)

                texto_descricao = tk.Label(JEC, text=f"{desc}", **config_text1)
                texto_descricao.place(x=20, y=200)

            cursor.close()
            conexao.close()
        else:
            print("Erro", "Não foi possível conectar ao banco de dados.")
    except Exception as e:
        print("Erro", f"Ocorreu um erro ao salvar: {e}")

    def salvarDados():

        vagas = vaga_entry.get()
        carga_horaria = carga_entry.get()
        descricao = descricao_entry.get()

        # Verificando se os dados não estão vazios
        if not vagas and not carga_horaria and not descricao:
            messagebox.showwarning("Aviso", "Nenhum campo foi preenchido para atualização.")
            return

        try:
            conexao = conexaoBanco()
            if conexao:
                cursor = conexao.cursor()

                update_values = []
                update_query = "UPDATE curso SET "
                if vagas:
                    update_query += "vagas = %s, "
                    update_values.append(vagas)
                if carga_horaria:
                    update_query += "carga_horaria = %s, "
                    update_values.append(carga_horaria)
                if descricao:
                    update_query += "descricao = %s, "
                    update_values.append(descricao)

                # Remove a vírgula final, caso algum campo não tenha sido alterado
                if update_values:
                    update_query = update_query.rstrip(", ")
                    update_query += " WHERE nome = %s"
                    update_values.append(nome)
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

                JEC.destroy()
            else:
                messagebox.showerror("Erro", "Não foi possível conectar ao banco de dados.")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao salvar: {e}")

    # Botão para registrar
    def deletarDados():
        try:
            conexao = conexaoBanco()
            if conexao:
                cursor = conexao.cursor()

                cursor.execute("DELETE FROM curso WHERE nome = %s", (nome,))

                conexao.commit()

                cursor.close()
                conexao.close()
                JEC.quit()
                JEC.destroy()
            else:
                print("Erro: Não foi possível conectar ao banco de dados.")
        except Exception as e:
            print(f"Erro ao deletar curso: {e}")

    bntDedeletar = tk.Button(JEC, text="Deletar", **config_botao, command=deletarDados)
    bntDedeletar.place(x=20, y=260)
    bntDeRegistro = tk.Button(JEC, text="Editar", **config_botao, command=salvarDados)
    bntDeRegistro.place(x=475, y=260)
    JEC.mainloop()
