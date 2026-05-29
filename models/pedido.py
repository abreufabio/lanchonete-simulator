from database import Database

class Pedido:
    def __init__(self):
        self.db = Database()

    def cadastrar(self, cliente, lanche, quantidade, status):
        query = """
            INSERT INTO pedidos (cliente, lanche, quantidade, status)
            VALUES (%s, %s, %s, %s) 
        """
        params = (cliente, lanche, quantidade, status)
        result = self.db.execute_query(query, params)
        return result is not None
    
    def listar_todos(self):
        query = "SELECT * FROM pedidos ORDER BY id DESC"
        return self.db.fetch_all(query)
    
    def buscar_por_id(self, pedido_id):
        query = "SELECT * FROM pedidos WHERE id = %s"
        params = (pedido_id,)
        return self.db.fetch_one(query, params)
    
    def editar(self, pedido_id, cliente, lanche, quantidade, status):
        query = """
            UPDATE pedidos 
            SET cliente = %s, lanche = %s, quantidade = %s, status = %s
            WHERE id = %s
        """
        params = (cliente, lanche, quantidade, status, pedido_id)
        result = self.db.execute_query(query, params)
        return result is not None

    def deletar(self, pedido_id):
        query = "DELETE FROM pedidos WHERE id = %s"
        params = (pedido_id,)
        result = self.db.execute_query(query, params)
        return result is not None
    
    def alterar_status(self, pedido_id, status):
        query = "UPDATE pedidos SET status = %s WHERE id = %s"
        params = (status, pedido_id)  # CORRIGIDO: variável correta
        result = self.db.execute_query(query, params)
        return result is not None