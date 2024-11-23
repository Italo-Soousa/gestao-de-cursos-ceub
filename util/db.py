import mysql.connector

class SQL:
    def __init__(self, servidor='localhost', user='root', password='ceub123', esquema='test'):
        self.conexao = mysql.connector.connect(host=servidor, user=user, password=password, database=esquema)

        cursor = self.conexao.cursor()

        cursor.close()
        self.conexao.close()
