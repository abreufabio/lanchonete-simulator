from database import Database

class Pedido:
    def __init__(self):
        self.db = Database()

    def criar_tabela(self):
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
        result = self.db.execute_query(query)
        return result is not None

    def cadastrar(self, cliente, lanche, quantidade, status):
        """Cadastra um novo pedido"""
        query = """
            INSERT INTO pedidos (cliente, lanche, quantidade, status)
            VALUES (%s, %s, %s, %s) 
        """
        params = (cliente, lanche, quantidade, status)
        result = self.db.execute_query(query, params)
        return result is not None
    
    def listar_todos(self):
        """Lista todos os pedidos ordenados por ID decrescente"""
        query = "SELECT * FROM pedidos ORDER BY id DESC"
        return self.db.fetch_all(query)
    
    def buscar_por_id(self, pedido_id):
        """Busca um pedido pelo ID"""
        query = "SELECT * FROM pedidos WHERE id = %s"
        params = (pedido_id,)
        return self.db.fetch_one(query, params)
    
    def editar(self, pedido_id, cliente, lanche, quantidade, status):
        """Edita um pedido existente"""
        query = """
            UPDATE pedidos 
            SET cliente = %s, lanche = %s, quantidade = %s, status = %s
            WHERE id = %s
        """
        params = (cliente, lanche, quantidade, status, pedido_id)
        result = self.db.execute_query(query, params)
        return result is not None

    def deletar(self, pedido_id):
        """Deleta um pedido"""
        query = "DELETE FROM pedidos WHERE id = %s"
        params = (pedido_id,)
        result = self.db.execute_query(query, params)
        return result is not None
    
    def alterar_status(self, pedido_id, status):
        """Altera o status de um pedido"""
        query = "UPDATE pedidos SET status = %s WHERE id = %s"
        params = (status, pedido_id)
        result = self.db.execute_query(query, params)
        return result is not None
    
    def buscar_por_status(self, status):
        """Busca pedidos por status"""
        query = "SELECT * FROM pedidos WHERE status = %s ORDER BY id DESC"
        params = (status,)
        return self.db.fetch_all(query)
    
    def buscar_por_cliente(self, cliente):
        """Busca pedidos por nome do cliente"""
        query = "SELECT * FROM pedidos WHERE cliente LIKE %s ORDER BY id DESC"
        params = (f'%{cliente}%',)
        return self.db.fetch_all(query)
    
    def contar_pedidos(self):
        """Conta o total de pedidos"""
        query = "SELECT COUNT(*) as total FROM pedidos"
        result = self.db.fetch_one(query)
        return result['total'] if result else 0
    
    def contar_pedidos_por_status(self, status):
        """Conta pedidos por status"""
        query = "SELECT COUNT(*) as total FROM pedidos WHERE status = %s"
        params = (status,)
        result = self.db.fetch_one(query, params)
        return result['total'] if result else 0
    
    def deletar_todos(self):
        """Deleta todos os pedidos (cuidado!)"""
        query = "DELETE FROM pedidos"
        result = self.db.execute_query(query)
        return result is not None