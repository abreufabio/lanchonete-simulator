import mysql.connector
from mysql.connector import Error
import hashlib

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

    # ==================== MÉTODOS PARA TABELA DE PEDIDOS ====================
    
    def criar_tabela_pedidos(self):
        """Cria a tabela de pedidos se não existir"""
        query = """
            CREATE TABLE IF NOT EXISTS pedidos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                cliente VARCHAR(100) NOT NULL,
                lanche VARCHAR(100) NOT NULL,
                quantidade INT NOT NULL,
                status VARCHAR(50) DEFAULT 'Pendente',
                data_pedido TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        return self.execute_query(query)
    
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
    
    # ==================== MÉTODOS PARA TABELA DE USUÁRIOS (LOGIN) ====================
    
    def criar_tabela_usuarios(self):
        """Cria a tabela de usuários se não existir"""
        query = """
            CREATE TABLE IF NOT EXISTS usuarios (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                senha VARCHAR(255) NOT NULL,
                data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        return self.execute_query(query)
    
    @staticmethod
    def hash_senha(senha):
        """Gera hash da senha usando SHA-256"""
        return hashlib.sha256(senha.encode()).hexdigest()
    
    def criar_usuario_admin(self):
        """Cria um usuário admin padrão se não existir nenhum usuário"""
        # Verificar se já existe algum usuário
        query_count = "SELECT COUNT(*) as total FROM usuarios"
        result = self.fetch_one(query_count)
        
        if result and result['total'] == 0:
            # Criar usuário admin padrão
            senha_hash = self.hash_senha('admin123')
            query_insert = """
                INSERT INTO usuarios (nome, email, senha)
                VALUES (%s, %s, %s)
            """
            self.execute_query(query_insert, ('Administrador', 'admin@lanchonete.com', senha_hash))
            print("=" * 50)
            print("✅ USUÁRIO ADMIN CRIADO COM SUCESSO!")
            print(f"   Email: admin@lanchonete.com")
            print(f"   Senha: admin123")
            print("=" * 50)
            return True
        return False
    
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
        """Cadastra um novo usuário no sistema"""
        # Verificar se email já existe
        query_check = "SELECT id FROM usuarios WHERE email = %s"
        existe = self.fetch_one(query_check, (email,))
        
        if existe:
            return False, "Email já cadastrado"
        
        # Cadastrar novo usuário
        senha_hash = self.hash_senha(senha)
        query_insert = """
            INSERT INTO usuarios (nome, email, senha)
            VALUES (%s, %s, %s)
        """
        resultado = self.execute_query(query_insert, (nome, email, senha_hash))
        
        if resultado:
            return True, "Usuário cadastrado com sucesso"
        return False, "Erro ao cadastrar usuário"
    
    def buscar_usuario_por_id(self, usuario_id):
        """Busca um usuário pelo ID"""
        query = "SELECT id, nome, email FROM usuarios WHERE id = %s"
        return self.fetch_one(query, (usuario_id,))
    
    def buscar_usuario_por_email(self, email):
        """Busca um usuário pelo email"""
        query = "SELECT id, nome, email FROM usuarios WHERE email = %s"
        return self.fetch_one(query, (email,))
    
    def atualizar_senha(self, usuario_id, nova_senha):
        """Atualiza a senha de um usuário"""
        nova_senha_hash = self.hash_senha(nova_senha)
        query = "UPDATE usuarios SET senha = %s WHERE id = %s"
        return self.execute_query(query, (nova_senha_hash, usuario_id))
    
    def listar_todos_usuarios(self):
        """Lista todos os usuários (apenas para administradores)"""
        query = "SELECT id, nome, email, data_cadastro FROM usuarios ORDER BY data_cadastro DESC"
        return self.fetch_all(query)
    
    def deletar_usuario(self, usuario_id):
        """Deleta um usuário do sistema"""
        query = "DELETE FROM usuarios WHERE id = %s"
        return self.execute_query(query, (usuario_id,))

# ==================== FUNÇÕES DE INICIALIZAÇÃO ====================

def init_database():
    """Inicializa o banco de dados e cria as tabelas necessárias"""
    db = Database()
    
    # Criar tabela de pedidos
    db.criar_tabela_pedidos()
    
    # Criar tabela de usuários
    db.criar_tabela_usuarios()
    
    # Criar usuário admin padrão
    db.criar_usuario_admin()
    
    print("✅ Banco de dados inicializado com sucesso!")

# Criar uma instância global do Database para ser usada em toda a aplicação
db_instance = Database()