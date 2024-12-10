import tkinter as tk
from util.db import conexaoBanco
from tkinter import messagebox

def Criar(cor0,texto,cor3):
    JGC = tk.Tk()
    JGC.title("Criar Curso")
    JGC.geometry("600x210")
    JGC.configure(bg=cor0)
    JGC.resizable(False, False)

    config_text = {
        'font': ("Arial", 13, "bold"),
        'fg': texto,
        'bg': cor0
    }


    # Exibindo o título com o nome do curso
    texto_nome = tk.Label(JGC, text=f"Cursos: ", **config_text)
    texto_nome.place(x=20, y=20)
    nome_entry = tk.Entry(JGC, font=("Arial", 13), width=20,bg=cor3, bd=0, highlightthickness=0)
    nome_entry.place(x=140, y=20)

    # Vagas
    texto_vagas = tk.Label(JGC, text="Vagas:", **config_text)
    texto_vagas.place(x=20, y=50)
    vaga_entry = tk.Entry(JGC, font=("Arial", 13), width=20,bg=cor3, bd=0, highlightthickness=0)
    vaga_entry.place(x=140, y=50)

    # Dias
    texto_carga_horaria = tk.Label(JGC, text="carga_horaria:", **config_text)
    texto_carga_horaria.place(x=20, y=80)
    carga_entry = tk.Entry(JGC, font=("Arial", 13), width=20,bg=cor3, bd=0, highlightthickness=0)
    carga_entry.place(x=140, y=80)

    # Descrição
    texto_descricao = tk.Label(JGC, text="Descrição:", **config_text)
    texto_descricao.place(x=250, y=110)

    descricao_entry = tk.Entry(JGC, font=("Arial", 13), width=62,bg=cor3, bd=0, highlightthickness=0)
    descricao_entry.place(x=20, y=140)

    def salvarDados():
        # Obtém os valores dos campos
        nome = nome_entry.get()
        vagas = vaga_entry.get()
        carga_horaria = carga_entry.get()
        descricao = descricao_entry.get()

        # Valida se todos os campos estão preenchidos
        if not nome or not carga_horaria or not vagas or not descricao:
            messagebox.showerror("Erro", "Todos os campos são obrigatórios!")
            return

        try:
            # Conecta ao banco usando o util.db
            conexao = conexaoBanco()
            if conexao:
                cursor = conexao.cursor()

                # Insere os dados na tabela "usuarios"
                cursor.execute("""
                            INSERT INTO curso (nome, vagas, carga_horaria, descricao) 
                            VALUES (%s, %s, %s, %s)
                        """, (nome, vagas, carga_horaria, descricao))

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
    # Botão para registrar
    bntDeRegistro = tk.Button(JGC,font= ("Arial", 10, "bold"),text="Criar",bg= "#363636",fg= texto,relief= "flat",activebackground=cor3,width= 12,command=salvarDados)
    bntDeRegistro.place(x=475, y=170)
    JGC.mainloop()
