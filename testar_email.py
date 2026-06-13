# testar_email.py
from utils.email_utils import email_utils
import secrets
import string

def gerar_token_valido():
    """Gera um token hexadecimal válido de 64 caracteres"""
    # Método 1: Usar secrets para gerar token aleatório
    token = secrets.token_hex(32)  # 32 bytes = 64 caracteres hex
    return token

print("Testando envio de email...")

# Gerar token válido automaticamente
token_valido = gerar_token_valido()
print(f"Token gerado: {token_valido}")
print(f"Tamanho do token: {len(token_valido)} caracteres")

resultado = email_utils.enviar_email_recuperacao(
    email_destino="",  # Substitua por seu email
    token=token_valido,  # ← Usar token válido
    nome_usuario="Usuario Teste",
    horas_validade=1
)

if resultado:
    print("✅ Email processado com sucesso!")
else:
    print("❌ Falha no processamento do email!")