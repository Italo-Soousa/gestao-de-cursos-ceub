import tkinter as tk
from util.db import conexaoBanco
from tkinter import messagebox
from util.config import cor0, config_botao, config_text_box, config_text1


def Editar(nome):
    JEC = tk.Tk()
    JEC.title(f"Janela de Edição de Curso")
    JEC.geometry("600x370")
    JEC.configure(bg=cor0)
    JEC.resizable(False, False)
    vaga_entry = tk.Entry(JEC, **config_text_box, width=20)
    vaga_entry.place(x=20, y=80)
    carga_entry = tk.Entry(JEC, **config_text_box, width=20)
    carga_entry.place(x=20, y=140)
    professor_entry = tk.Entry(JEC, **config_text_box, width=20)
    professor_entry.place(x=20, y=200)
    descricao_entry = tk.Entry(JEC, **config_text_box, width=62)
    descricao_entry.place(x=20, y=280)
    try:
        conexao = conexaoBanco()
        if conexao:
            cursor = conexao.cursor()

            cursor.execute("SELECT vagas, carga_horaria, descricao,id_curso FROM cursos WHERE nome = %s", (nome,))
            resultado = cursor.fetchone()

            if resultado:
                vag, carga_horaria, desc,id_c= resultado
                global id_curso
                id_curso = id_c
                texto_informativo = tk.Label(JEC, text=f"Nome Do Curso: {nome}", **config_text1)
                texto_informativo.place(x=20, y=20)
                texto_vagas = tk.Label(JEC, text=f"Vagas Do Curso: {vag}", **config_text1)
                texto_vagas.place(x=20, y=50)
                texto_carga = tk.Label(JEC, text=f"Carga Horaria Do Curso: {carga_horaria} Horas", **config_text1)
                texto_carga.place(x=20, y=110)
                texto_Professor = tk.Label(JEC, text="Login do Professor:", **config_text1)
                texto_Professor.place(x=20, y=170)
                texto_descricao = tk.Label(JEC, text=f"{desc}", **config_text1,wraplength=580)
                texto_descricao.place(x=20, y=230)

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
        login = professor_entry.get()  # Pega o login inserido

        if not vagas and not carga_horaria and not descricao and not login:
            messagebox.showwarning("Aviso", "Nenhum campo foi preenchido para atualização.")
            return

        try:
            conexao = conexaoBanco()
            if conexao:
                cursor = conexao.cursor()

                # Atualiza os dados do curso
                update_values = []
                update_query = "UPDATE cursos SET "
                if vagas:
                    update_query += "vagas = %s, "
                    update_values.append(vagas)
                if carga_horaria:
                    update_query += "carga_horaria = %s, "
                    update_values.append(carga_horaria)
                if descricao:
                    update_query += "descricao = %s, "
                    update_values.append(descricao)

                if update_values:
                    update_query = update_query.rstrip(", ")
                    update_query += " WHERE nome = %s"
                    update_values.append(nome)
                    cursor.execute(update_query, tuple(update_values))
                    conexao.commit()

                # Verifica se o login do professor existe
                if login:
                    cursor.execute("SELECT id_perfis, tipo_usuario FROM perfis WHERE login = %s", (login,))
                    resultado = cursor.fetchone()
                    if not resultado:
                        messagebox.showerror("Erro", "Login de professor inválido.")
                        return

                    id_perfis, tipo_usuario = resultado
                    if tipo_usuario == "professor":
                        # Insere o relacionamento do curso com o professor na tabela inscricoes
                        cursor.execute(
                            "INSERT INTO inscricoes (id_curso, id_perfis) VALUES ((SELECT id_curso FROM cursos WHERE nome = %s), %s) ON DUPLICATE KEY UPDATE id_perfis = %s",
                            (nome, id_perfis, id_perfis)
                        )
                        conexao.commit()
                        messagebox.showinfo("Sucesso", "Dados atualizados e inscrição realizada com sucesso!")
                    else:
                        messagebox.showerror("Erro", "Esse usuário não é um professor.")
                else:
                    messagebox.showwarning("Aviso", "Nenhum login de professor fornecido.")

                cursor.close()
                conexao.close()

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
                cursor.execute("DELETE FROM inscricoes WHERE id_curso = %s", (id_curso,))
                cursor.execute("DELETE FROM cursos WHERE nome = %s", (nome,))
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
    bntDedeletar.place(x=20, y=310)
    bntDeRegistro = tk.Button(JEC, text="Editar", **config_botao, command=salvarDados)
    bntDeRegistro.place(x=475, y=310)
    JEC.mainloop()
