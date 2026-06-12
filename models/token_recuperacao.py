from database import db_instance
import secrets
import string
import hashlib

class TokenRecuperacao:
    @staticmethod
    def gerar_token():
        # ========= METODO PARA GERAR UM TOKEN ALEATORIO
        alphabet = string.ascii_letters + string.digits
        token = ''.join(secrets.choice(alphabet) for _ in range(32))
        return token
    @staticmethod
    def criar_token(usurio_id, horas_validade):
        # ========= CRIA E SALVA UM TOKEN DE RECUPERAÇÃO
        token = TokenRecuperacao.gerar_token()
        token_hash = hashlib.sha256(token.encode()).hexdigest()

        resultado = db_instance.salvar_token(usuario_id, token_hash, horas_validade)
        if resultado:
            return token # ====== AQUI VAI RETORNAR O TOKEN ORIGINAL E ENVIAR PARA O EMAIL
        return None
    @staticmethod
    def validar_token(token):
        # ========= VALIDAR UM TOKEN RECUPERAÇÃO
        token_hash = hashlib.sha256(token.encode()).hexdigest()
        return  db_instance.buscar_token(token_hash)
    
    @staticmethod
    def usar_token(token):
        # ========= MARCA UM TOKEN COMO USADO
        token_hash =hashlib.sha256(token.encode()).hexdigest()
        return db_instance.marcar_token_usado(token_hash)