import tkinter as tk

def Criar(cor0,texto,cor3):
    JGC = tk.Tk()
    JGC.title("Criar Curso")
    JGC.geometry("600x350")
    JGC.configure(bg=cor0)
    JGC.resizable(False, False)

    config_text = {
        'font': ("Arial", 13, "bold"),
        'fg': texto,
        'bg': cor0
    }

    # Exibindo o título com o nome do curso
    texto_nome = tk.Label(JGC, text=f"Cursos: ", **config_text)
    texto_nome.place(x=20, y=30)
    nome_entry = tk.Entry(JGC, font=("Arial", 13), width=20,bg=cor3, bd=0, highlightthickness=0)
    nome_entry.place(x=140, y=30)

    # Vagas
    texto_vagas = tk.Label(JGC, text="Vagas:", **config_text)
    texto_vagas.place(x=20, y=60)
    vaga_entry = tk.Entry(JGC, font=("Arial", 13), width=20,bg=cor3, bd=0, highlightthickness=0)
    vaga_entry.place(x=140, y=60)

    # Dias
    texto_dias = tk.Label(JGC, text="Dias:", **config_text)
    texto_dias.place(x=20, y=90)
    dias_entry = tk.Entry(JGC, font=("Arial", 13), width=20,bg=cor3, bd=0, highlightthickness=0)
    dias_entry.place(x=140, y=90)

    # Horas
    texto_horas = tk.Label(JGC, text="Horas:", **config_text)
    texto_horas.place(x=20, y=120)
    horas_entry = tk.Entry(JGC, font=("Arial", 13), width=20,bg=cor3, bd=0, highlightthickness=0)
    horas_entry.place(x=140, y=120)

    # Data de início
    texto_data_inicio = tk.Label(JGC, text="Data de Início:", **config_text)
    texto_data_inicio.place(x=20, y=150)
    data_inicio_entry = tk.Entry(JGC, font=("Arial", 13), width=20,bg=cor3, bd=0, highlightthickness=0)
    data_inicio_entry.place(x=140, y=150)

    # Descrição
    texto_descricao = tk.Label(JGC, text="Descrição:", **config_text)
    texto_descricao.place(x=250, y=180)

    descricao_entry = tk.Entry(JGC, font=("Arial", 13), width=62,bg=cor3, bd=0, highlightthickness=0)
    descricao_entry.place(x=20, y=210)

    JGC.mainloop()
