import mysql.connector

def conexaoBanco():
    try:
        conexao = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Brazil123',
            database='bd_gestaoCursos'
        )
        return conexao
    except mysql.connector.Error as e: # Error aponta o erro no terminal que passa para a variável
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None