import mysql.connector
from mysql.connector import Error
import hashlib
import re
from datetime  import datetime, timedelta

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

    # ==================== CRUD PARA TABELA DE PEDIDOS ====================
    
    def listar_pedidos(self):
        """Lista todos os pedidos"""
        query = "SELECT * FROM pedidos ORDER BY data_pedido DESC"
        return self.fetch_all(query)
    
    def buscar_pedido_por_id(self, pedido_id):
        """Busca um pedido pelo ID"""
        query = "SELECT * FROM pedidos WHERE id = %s"
        return self.fetch_one(query, (pedido_id,))
    
    def cadastrar_pedido(self, cliente, lanche, quantidade, status):
        """Cadastra um novo pedido"""
        query = """
            INSERT INTO pedidos (cliente, lanche, quantidade, status)
            VALUES (%s, %s, %s, %s)
        """
        return self.execute_query(query, (cliente, lanche, quantidade, status))
    
    def editar_pedido(self, pedido_id, cliente, lanche, quantidade, status):
        """Edita um pedido existente"""
        query = """
            UPDATE pedidos 
            SET cliente = %s, lanche = %s, quantidade = %s, status = %s
            WHERE id = %s
        """
        return self.execute_query(query, (cliente, lanche, quantidade, status, pedido_id))
    
    def deletar_pedido(self, pedido_id):
        """Deleta um pedido"""
        query = "DELETE FROM pedidos WHERE id = %s"
        return self.execute_query(query, (pedido_id,))
    
    def alterar_status_pedido(self, pedido_id, status):
        """Altera o status de um pedido"""
        query = "UPDATE pedidos SET status = %s WHERE id = %s"
        return self.execute_query(query, (status, pedido_id))
    
    # ==================== CRUD OS PARA TABELA DE USUÁRIOS (LOGIN) ====================
    
    
    def autenticar_usuario(self, email, senha):
        """Autentica um usuário e retorna seus dados se bem-sucedido"""
        # Buscar usuário pelo email
        query = "SELECT id, nome, email, senha FROM usuarios WHERE email = %s"
        usuario = self.fetch_one(query, (email,))
        
        if usuario:
            # Verificar se a senha está correta
            senha_hash = self.hash_senha(senha)
            if senha_hash == usuario['senha']:
                # Retornar dados do usuário (sem a senha)
                return {
                    'id': usuario['id'],
                    'nome': usuario['nome'],
                    'email': usuario['email']
                }
        return None
    
    def cadastrar_usuario(self, nome, email, senha):
        #Cadastro de um novo usuario, e validações
        #Validação de campos
        if not nome or not nome.strip():
            return False, "Nome não pode estar em branco"
        if not email or not email.strip():
            return False, "Email não pode estar em branco"
        if not senha:
            return False, "Senha não pode estar em branco"
        
        #Verificação se o email já existe
        query_check = "Select id from usuarios where email = %s"
        existe = self.fetch_one(query_check, (email, ))
        if existe:
            return False, "Email já cadastrado"
        
        #Verifica se a senha é forte usando o metedo criado de vreficação
        senha_valida, msg = self.validar_senha_forte(senha)
        if not senha_valida:
            return False, msg
        
        # ========== Cadastro
        senha_hash = self.hash_senha(senha)
        query_insert = """
            insert into usuarios (nome, email, senha, ultima_alteracao_senha)
            values (%s, %s, %s, %s)
        """
        resultado = self.execute_query(query_insert, (nome.strip(), email.strip(), senha_hash))
        if resultado:
            return True, "Usuario cadastrado com sucesso"
        return False, "Erro ao cadastrar usuario"
    
    #Atualização da senha
    def atualizar_senha(self, usuario_id, nova_senha):
        senha_valida, msg = self.validar_senha_forte(nova_senha)
        if not senha_valida:
            return False, msg
        nova_senha_hash = self.hash_senha(nova_senha)
        query = "update usuarios set senha = %s, ultima_alteracao_senha = now() where id = %s"
        resultado = self.execute_query(query, (nova_senha_hash, usuario_id))

        if resultado:
            return True, "Senha alterada com sucesso!"
        return False, "Erro ao alterar senha"
    
    def buscar_usuario_por_id(self, usuario_id):
        """Busca um usuário pelo ID"""
        query = "SELECT id, nome, email FROM usuarios WHERE id = %s"
        return self.fetch_one(query, (usuario_id,))
    
    def buscar_usuario_por_email(self, email):
        """Busca um usuário pelo email"""
        query = "SELECT id, nome, email FROM usuarios WHERE email = %s"
        return self.fetch_one(query, (email,))
    
    # ==================== FUNÇÕES DO TOKEN  ===========================

    def salvar_token(self, usuario_id, token_hash, horas_validade=1):
        expiracao = datetime.now() + timedelta(hours=horas_validade)
        query = """
            insert into tokens_recupercao (usuario_id, token_hash, expiracao)
            values(%s, %s, %s)
        """
        return self.execute_query(query, (usuario_id, token_hash, expiracao))

    def buscar_token(self, token_hash):
        query = """
            select * from token_recuperacao
            where token_hash = %s and usado = false and expiracao > now()
        """
        return self.fetch_one(query, (token_hash))

    def marcar_token_usado(self, token_hash):
        query = "update token_recuperacao set usado = true where token_hash = %s"

    def limpar_tokens_expirados(self):
        query = "delete from token_recupercao where expiracao < now() or usado = true"

    # ==================== FUNÇÕES DE SENHAS FORTE ======================

                # ===== Criteios são:
                # ===== Minimo 8 caracteres
                # ===== Pelo menos uma letra maiuscula
                # ===== Pelo menos uma letra minuscula
                # ===== Pelo menos um numero 
                # ===== Pelo menos um caractere especial (!@#$%¨&*)

    @staticmethod
    def hash_senha(senha):
        return hashlib.sha256(senha.encode()).hexdigest()

    def validar_senha_forte():
        if len(senha) < 8:
            return False, "A senha deve ter no minimo 8 caracteres"
        if not re.search(r'[A-Z]', senha):
            return False, "A senha deve possuir pelo menos uma letra maiuscula"
        if not re.search(r'[a-z]', senha):
            return False, "A senha deve possuir pelo menos uma letra minucula"
        if not re.search(r'[0-9]', senha):
            return False, "A senha deve possuir pelo menos um número"
        if not re.search(r'[!@#$%¨&*():><,.;|{}-=+_§ºª~~^]', senha):
            return False, "A senha deve possuir pelo menos um caractere especial (!@#$%¨&*():> etc)"
        return True, "Senha forte"
        
    # ==================== FUNÇÕES DE INICIALIZAÇÃO ====================

    def init_database():
        """Inicializa o banco de dados e cria as tabelas necessárias"""
        db = Database()
        
        print("✅ Banco de dados inicializado com sucesso!")
    
    # Criar uma instância global do Database para ser usada em toda a aplicação
def init_database():
    """Inicializa o banco de dados"""
    db = Database()
    print("✅ Banco de dados inicializado com sucesso!")
db_instance = Database()
