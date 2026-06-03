from database import db_instance

class Usuario:
    def __init__(self, id=None, nome=None, email=None):
        self.id = id
        self.nome = nome
        self.email = email
    
    @staticmethod
    def autenticar(email, senha):
        """Autentica um usuário"""
        resultado = db_instance.autenticar_usuario(email, senha)
        if resultado:
            return Usuario(
                id=resultado['id'],
                nome=resultado['nome'],
                email=resultado['email']
            )
        return None
    
    @staticmethod
    def cadastrar(nome, email, senha):
        """Cadastra um novo usuário"""
        return db_instance.cadastrar_usuario(nome, email, senha)
    
    @staticmethod
    def buscar_por_id(id_usuario):
        """Busca um usuário pelo ID"""
        resultado = db_instance.buscar_usuario_por_id(id_usuario)
        if resultado:
            return Usuario(
                id=resultado['id'],
                nome=resultado['nome'],
                email=resultado['email']
            )
        return None
    
    def to_dict(self):
        """Converte o objeto para dicionário"""
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email
        }