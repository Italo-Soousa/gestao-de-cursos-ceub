import tkinter as tk
from util.db import conexaoBanco

def Info(cor0, texto, nome):
    JGC = tk.Tk()
    JGC.title(f"{nome}")
    JGC.geometry("600x170")
    JGC.configure(bg=cor0)
    JGC.resizable(False, False)

    config_text = {
        'font': ("Arial", 13, "bold"),
        'fg': texto,
        'bg': cor0
    }

    try:
        # Conecta ao banco usando o util.db
        conexao = conexaoBanco()
        if conexao:
            cursor = conexao.cursor()

            # Consulta as informações do curso pelo nome
            cursor.execute("SELECT vagas, carga_horaria, descricao FROM curso WHERE nome = %s", (nome,))
            resultado = cursor.fetchone()

            if resultado:
                vagas,carga_horaria, descricao= resultado

                # Exibindo o título com o nome do curso
                texto_informativo = tk.Label(JGC, text=f"Cursos: {nome}", **config_text)
                texto_informativo.place(x=20, y=20)

                # Vagas
                texto_vagas = tk.Label(JGC, text=f"Vagas: {vagas}", **config_text)
                texto_vagas.place(x=20, y=50)

                # Dias
                texto_dias = tk.Label(JGC, text=f"carga_horaria: {carga_horaria}", **config_text)
                texto_dias.place(x=20, y=80)

                # Descrição
                texto_descricao = tk.Label(JGC, text="Descrição:", **config_text)
                texto_descricao.place(x=250, y=110)

                texto_descricao = tk.Label(JGC, text=f"{descricao}", **config_text)
                texto_descricao.place(x=20, y=140)

            cursor.close()
            conexao.close()
        else:
            print("Erro", "Não foi possível conectar ao banco de dados.")
    except Exception as e:
        print("Erro", f"Ocorreu um erro ao salvar: {e}")
    JGC.mainloop()
