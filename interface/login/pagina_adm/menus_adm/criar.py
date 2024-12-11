import tkinter as tk
from util.db import conexaoBanco
from tkinter import messagebox
from util.config import cor0, config_botao, config_text_box, config_text1


def Criar():
    JGC = tk.Tk()
    JGC.title("Criar Curso")
    JGC.geometry("600x310")
    JGC.configure(bg=cor0)
    JGC.resizable(False, False)

    texto_nome = tk.Label(JGC, text=f"Nome Do Curso: ", **config_text1)
    texto_nome.place(x=20, y=20)
    nome_entry = tk.Entry(JGC, **config_text_box, width=20)
    nome_entry.place(x=20, y=50)

    texto_vagas = tk.Label(JGC, text="Vagas Do Curso:", **config_text1)
    texto_vagas.place(x=20, y=80)
    vaga_entry = tk.Entry(JGC, **config_text_box, width=20)
    vaga_entry.place(x=20, y=110)

    texto_carga_horaria = tk.Label(JGC, text="Carga Horaria Do Curso:", **config_text1)
    texto_carga_horaria.place(x=20, y=140)
    carga_entry = tk.Entry(JGC, **config_text_box, width=20)
    carga_entry.place(x=20, y=170)

    texto_descricao = tk.Label(JGC, text="Descrição Do Curso:", **config_text1)
    texto_descricao.place(x=200, y=200)

    descricao_entry = tk.Entry(JGC, **config_text_box, width=62)
    descricao_entry.place(x=20, y=230)

    def salvarDados():
        nome = nome_entry.get()
        vagas = vaga_entry.get()
        carga_horaria = carga_entry.get()
        descricao = descricao_entry.get()

        # Valida se todos os campos estão preenchidos
        if not nome or not carga_horaria or not vagas:
            messagebox.showerror("Erro", "Todos os campos são obrigatórios!")
            return

        try:
            conexao = conexaoBanco()
            if conexao:
                cursor = conexao.cursor()

                cursor.execute("INSERT INTO curso (nome, vagas, carga_horaria, descricao) VALUES (%s, %s, %s, %s)",
                               (nome, vagas, carga_horaria, descricao))

                # Confirma as alterações no banco
                conexao.commit()
                messagebox.showinfo("Sucesso", "Registro salvo com sucesso!")

                # Fecha a conexão e o cursor
                cursor.close()
                conexao.close()

                # Fecha a janela de registro
                JGC.destroy()
            else:
                messagebox.showerror("Erro", "Não foi possível conectar ao banco de dados.")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao salvar: {e}")

    bntDeRegistro = tk.Button(JGC, text="Criar", **config_botao, command=salvarDados)
    bntDeRegistro.place(x=475, y=260)
    JGC.mainloop()
