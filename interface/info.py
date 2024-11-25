import tkinter as tk

def Info(cor0,texto,nome):
    JGC = tk.Tk()
    JGC.title(f"{nome}")
    JGC.geometry("600x350")
    JGC.configure(bg=cor0)
    JGC.resizable(False, False)

    config_text = {
        'font': ("Arial", 13, "bold"),
        'fg': texto,
        'bg': cor0
    }
    # Exibindo o título com o nome do curso
    texto_informativo = tk.Label(JGC, text=f"Cursos: {nome}", **config_text)
    texto_informativo.place(x=80, y=20)

    # Vagas
    texto_vagas = tk.Label(JGC, text="Vagas:", **config_text)
    texto_vagas.place(x=20, y=60)

    # Dias
    texto_dias = tk.Label(JGC, text="Dias:", **config_text)
    texto_dias.place(x=20, y=90)

    # Horas
    texto_horas = tk.Label(JGC, text="Horas:", **config_text)
    texto_horas.place(x=20, y=120)

    # Data de início
    texto_data_inicio = tk.Label(JGC, text="Data de Início:", **config_text)
    texto_data_inicio.place(x=20, y=150)

    # Descrição
    texto_descricao = tk.Label(JGC, text="Descrição:", **config_text)
    texto_descricao.place(x=250, y=180)

    texto_descricao = tk.Label(JGC, text="Descrição:", **config_text)
    texto_descricao.place(x=0, y=210)

    JGC.mainloop()
