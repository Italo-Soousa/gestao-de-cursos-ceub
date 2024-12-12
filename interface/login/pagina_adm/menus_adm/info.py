import tkinter as tk
from util.db import conexaoBanco
from util.config import cor0, config_text1


def Info(nome):
    JIC = tk.Tk()
    JIC.title("Janela de Informaçoes do Curso")
    JIC.geometry("600x190")
    JIC.configure(bg=cor0)
    JIC.resizable(False, False)

    try:
        # Conecta ao banco usando o util.db
        conexao = conexaoBanco()
        if conexao:
            cursor = conexao.cursor()

            # Consulta as informações do curso pelo nome
            cursor.execute("SELECT vagas, carga_horaria, descricao FROM cursos WHERE nome = %s", (nome,))
            resultado = cursor.fetchone()

            if resultado:
                vagas, carga_horaria, descricao = resultado

                # Exibindo o título com o nome do curso
                texto_informativo = tk.Label(JIC, text=f"Nome do Curso: {nome}", **config_text1)
                texto_informativo.place(x=20, y=20)

                # Vagas
                texto_vagas = tk.Label(JIC, text=f"Vagas do Curso: {vagas}", **config_text1)
                texto_vagas.place(x=20, y=50)

                # Dias
                texto_dias = tk.Label(JIC, text=f"Carga Horaria do Curso: {carga_horaria} Horas", **config_text1)
                texto_dias.place(x=20, y=80)

                # Descrição
                texto_descricao = tk.Label(JIC, text="Descrição do Curso:", **config_text1)
                texto_descricao.place(x=200, y=110)

                texto_descricao = tk.Label(JIC, text=f"{descricao}", **config_text1,wraplength=580)
                texto_descricao.place(x=20, y=140)

            cursor.close()
            conexao.close()
        else:
            print("Erro", "Não foi possível conectar ao banco de dados.")
    except Exception as e:
        print("Erro", f"Ocorreu um erro ao salvar: {e}")
    JIC.mainloop()
