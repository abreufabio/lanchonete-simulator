from database import db_instance
import secrets
import hashlib

class TokenRecuperacao:
    @staticmethod
    def gerar_token():
        # ========= METODO PARA GERAR UM TOKEN SHA 256 HEXADECIMAL DE 64 CARACTERES
        # secrets.token_hex(32) gera 64 caracteres hexadecimais
        token = secrets.token_hex(32)
        return token
    
    @staticmethod
    def criar_token(usuario_id, horas_validade=1):
        """Cria e salva um token de recuperação"""
        token = TokenRecuperacao.gerar_token()
        # Hash do token para armazenar no banco (segurança extra)
        token_hash = hashlib.sha256(token.encode()).hexdigest()

        resultado = db_instance.salvar_token(usuario_id, token_hash, horas_validade)
        if resultado:
            return token  # Retorna token original (64 caracteres hex)
        return None
    
    @staticmethod
    def validar_token(token):
        # Validação básica para evitar erros
        if not token or len(token) != 64:
            return None
        
        token_hash = hashlib.sha256(token.encode()).hexdigest()
        return db_instance.buscar_token(token_hash)
    
    @staticmethod
    def usar_token(token):
        # ============ Marca um token como usado
        token_hash = hashlib.sha256(token.encode()).hexdigest()
        return db_instance.marcar_token_usado(token_hash)