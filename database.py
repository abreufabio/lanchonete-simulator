import mysql.connector
from mysql.connector import Error

class Database:
    def __init__(self):
        self.config = {
            'host': 'localhost',
            'user': 'root',
            'password': 'Fabio123@',
            'database': 'lanchonete'
        }
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(**self.config)
            return self.connection
        except Error as e:
            print(f"Erro ao conectar com o banco de dados: {e}")
            return None

    def close(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()

    def execute_query(self, query, params=None):
        conn = self.connect()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute(query, params)
                conn.commit()
                return cursor
            except Error as e:
                print(f"Erro ao executar a consulta: {e}")
                return None
            finally:
                cursor.close()
                self.close()
        return None

    def fetch_all(self, query, params=None):
        conn = self.connect()
        if conn:
            cursor = conn.cursor(dictionary=True)
            try:
                cursor.execute(query, params)
                result = cursor.fetchall()
                return result
            except Error as e:
                print(f"Erro ao buscar dados: {e}")
                return []
            finally:
                cursor.close()
                self.close()
        return []

    def fetch_one(self, query, params=None):
        conn = self.connect()
        if conn:
            cursor = conn.cursor(dictionary=True)
            try:
                cursor.execute(query, params)
                result = cursor.fetchone()
                return result
            except Error as e:
                print(f"Erro ao buscar dados: {e}")
                return None
            finally:
                cursor.close()
                self.close()
        return None