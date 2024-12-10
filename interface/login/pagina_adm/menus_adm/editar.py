import tkinter as tk
from util.db import conexaoBanco
from tkinter import messagebox
def Editar(cor0, texto, nome,cor3):
    JGC = tk.Tk()
    JGC.title(f"{nome}")
    JGC.geometry("600x300")
    JGC.configure(bg=cor0)
    JGC.resizable(False, False)

    config_text = {
        'font': ("Arial", 13, "bold"),
        'fg': texto,
        'bg': cor0
    }
    vaga_entry = tk.Entry(JGC, font=("Arial", 13), width=20, bg=cor3, bd=0, highlightthickness=0)
    vaga_entry.place(x=20, y=80)
    carga_entry = tk.Entry(JGC, font=("Arial", 13), width=20, bg=cor3, bd=0, highlightthickness=0)
    carga_entry.place(x=20, y=140)
    descricao_entry = tk.Entry(JGC, font=("Arial", 13), width=62, bg=cor3, bd=0, highlightthickness=0)
    descricao_entry.place(x=20, y=230)
    try:
        # Conecta ao banco usando o util.db
        conexao = conexaoBanco()
        if conexao:
            cursor = conexao.cursor()

            # Consulta as informações do curso pelo nome
            cursor.execute("SELECT vagas, carga_horaria, descricao FROM curso WHERE nome = %s", (nome,))
            resultado = cursor.fetchone()

            if resultado:
                vag,carga_horaria, desc= resultado

                # Exibindo o título com o nome do curso
                texto_informativo = tk.Label(JGC, text=f"Cursos: {nome}", **config_text)
                texto_informativo.place(x=20, y=20)

                # Vagas
                texto_vagas = tk.Label(JGC, text=f"Vagas: {vag}", **config_text)
                texto_vagas.place(x=20, y=50)
                # Dias
                texto_carga  = tk.Label(JGC, text=f"carga_horaria: {carga_horaria}", **config_text)
                texto_carga .place(x=20, y=110)

                # Descrição
                texto_descricao = tk.Label(JGC, text="Descrição:", **config_text)
                texto_descricao.place(x=250, y=170)

                texto_descricao = tk.Label(JGC, text=f"{desc}", **config_text)
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
            # Conecta ao banco usando o util.db
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
                    update_query = update_query.rstrip(", ")  # Remove a vírgula extra no final
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
    bntDeRegistro.place(x=475, y=260)
    JGC.mainloop()
