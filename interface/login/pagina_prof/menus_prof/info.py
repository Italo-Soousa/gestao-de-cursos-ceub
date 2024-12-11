import tkinter as tk
from util.db import conexaoBanco
from interface.login.pagina_prof.menus_prof.avaliar_aluno import avaliar
from util.config import cor0, config_botao, config_text1


def Info(nome):
    JDI = tk.Tk()
    JDI.title("Janela de Informaçoes do Curso")
    JDI.geometry("600x310")
    JDI.configure(bg=cor0)
    JDI.resizable(False, False)
    # Variável para armazenar o aluno selecionado
    selected_student = None

    def on_student_click(event, student_id, y_position, alu_nome):
        global id
        global alunox
        id = student_id
        alunox = alu_nome
        nonlocal selected_student
        selected_student = student_id
        print(f"Aluno selecionado: {student_id}")

        # Destacar a linha selecionada
        # Remove o destaque anterior, se houver
        canvas.delete("highlight")
        canvas.create_rectangle(0, y_position - 10, 570, y_position + 10, outline="BLACK", width=2, tags="highlight")

    def Avaliar():
        avaliar.avaliar(id, id_curso, alunox)

    try:
        # Conecta ao banco usando o util.db
        conexao = conexaoBanco()
        if conexao:
            cursor = conexao.cursor()

            # Consulta as informações do curso pelo nome
            cursor.execute("SELECT vagas, carga_horaria, descricao, id_curso FROM curso WHERE nome = %s", (nome,))
            resultado = cursor.fetchone()

            if resultado:
                global id_curso
                vagas, carga_horaria, descricao, id_curso = resultado

                # Exibindo o título com o nome do curso
                texto_informativo = tk.Label(JDI,
                                             text=f"Cursos: {nome}    |    Vagas: {vagas}    |    Carga Horária: {carga_horaria}",
                                             **config_text1)
                texto_informativo.place(x=10, y=10)

                # Criar o canvas para exibir a tabela
                canvas = tk.Canvas(JDI, width=580, height=200, bg=cor0)
                canvas.place(x=10, y=50)

                # Buscar os IDs dos alunos inscritos no curso atual
                cursor.execute("SELECT id_perfis FROM inscricoes WHERE id_curso = %s", (id_curso,))
                ids_alunos = cursor.fetchall()

                if ids_alunos:
                    # Extrair os IDs em uma lista
                    ids_alunos = [id_aluno[0] for id_aluno in ids_alunos]

                    # Criar placeholders para a consulta IN
                    placeholders = ', '.join(['%s'] * len(ids_alunos))

                    # Etapa 2: Buscar nomes e verificar tipo de usuário "aluno"
                    query = f"SELECT id_perfis, nome FROM perfis WHERE id_perfis IN ({placeholders}) AND tipo_usuario = 'aluno'"
                    cursor.execute(query, tuple(ids_alunos))
                    alunos = cursor.fetchall()

                    cabecalho = ["ID", "Nome"]
                    y_position = 20
                    colunas_largura = [100, 400]

                    # Exibindo o cabeçalho da tabela
                    for i, coluna in enumerate(cabecalho):
                        canvas.create_text(10 + sum(colunas_largura[:i]), y_position, text=coluna,
                                           font=("Arial", 12, "bold"))

                    # Avançar para a próxima linha
                    y_position += 20

                    # Exibindo os dados dos alunos
                    for aluno in alunos:
                        id_aluno, nome_aluno = aluno
                        for i, dado in enumerate([id_aluno, nome_aluno]):
                            canvas.create_text(10 + sum(colunas_largura[:i]), y_position, text=dado, font=("Arial", 12))

                        # Corrigir a referência de id_aluno usando o lambda com argumento fixo
                        canvas.tag_bind(f"linha_{id_aluno}", "<Button-1>",
                                        lambda e, id_aluno=id_aluno, y_position=y_position: on_student_click(e,
                                                                                                             id_aluno,
                                                                                                             y_position,
                                                                                                             nome_aluno))

                        # Atribuindo um tag a cada linha para identificação
                        canvas.create_rectangle(10, y_position - 10, 580, y_position + 10, outline="", width=0,
                                                tags=f"linha_{id_aluno}")
                        y_position += 20  # Avançar para a próxima linha

            cursor.close()
            conexao.close()
        else:
            print("Erro", "Não foi possível conectar ao banco de dados.")
    except Exception as e:
        print("Erro", f"Ocorreu um erro ao salvar: {e}")
    # Botão para registrar
    bntDeRegistro = tk.Button(JDI, text="Avaliar", **config_botao, command=Avaliar)
    bntDeRegistro.place(x=475, y=180)
    JDI.mainloop()

    JDI.mainloop()
