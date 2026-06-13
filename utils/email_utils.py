import os
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmailUtils:
    def __init__(self):
        # ============ CONFIGURACOES DE SEGURANCA ============
        self.modo_teste = os.getenv('EMAIL_MODO_TESTE', 'True').lower() == 'true'
        self.smtp_server = os.getenv('EMAIL_SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('EMAIL_SMTP_PORT', 587))
        self.email_user = os.getenv('EMAIL_USER')
        self.email_password = os.getenv('EMAIL_PASSWORD')
        self.email_from = os.getenv('EMAIL_FROM', self.email_user)
        self.url_base = os.getenv('URL_BASE', 'http://localhost:5000')
        
        # Validacao de configuracao no modo real
        if not self.modo_teste:
            self._validar_configuracao_email()
    
    def _validar_configuracao_email(self):
        """Valida se as configuracoes de email estao presentes"""
        if not self.email_user or not self.email_password:
            raise ValueError(
                "Configuracoes de email nao encontradas! "
                "Configure as variaveis EMAIL_USER e EMAIL_PASSWORD no arquivo .env"
            )
    
    def _sanitizar_input(self, texto):
        """Sanitiza entradas para evitar injection"""
        if not texto:
            return ""
        # Remove caracteres potencialmente perigosos
        caracteres_perigosos = ['\r', '\n', '\x00', '\x1a']
        for char in caracteres_perigosos:
            texto = texto.replace(char, '')
        return texto.strip()
    
    def _validar_email(self, email):
        """Valida formato do email"""
        import re
        padrao = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(padrao, email) is not None
    
    def _gerar_html_email(self, nome_usuario, link_recuperacao, horas_validade=1):
        """Gera o corpo do email em HTML com CSS inline"""
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Recuperacao de Senha</title>
            <style>
                body {{
                    margin: 0;
                    padding: 0;
                    font-family: Arial, Helvetica, sans-serif;
                    background-color: #f4f4f4;
                }}
                .container {{
                    max-width: 600px;
                    margin: 20px auto;
                    background-color: #ffffff;
                    border-radius: 8px;
                    overflow: hidden;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }}
                .header {{
                    background-color: #2c3e50;
                    padding: 30px 20px;
                    text-align: center;
                }}
                .header h1 {{
                    color: #ffffff;
                    margin: 0;
                    font-size: 24px;
                    font-weight: normal;
                }}
                .content {{
                    padding: 40px 30px;
                    background-color: #ffffff;
                }}
                .greeting {{
                    font-size: 18px;
                    color: #333333;
                    margin-bottom: 20px;
                }}
                .message {{
                    color: #555555;
                    line-height: 1.6;
                    margin-bottom: 30px;
                }}
                .button-container {{
                    text-align: center;
                    margin: 35px 0;
                }}
                .button {{
                    background-color: #3498db;
                    color: #ffffff !important;
                    text-decoration: none;
                    padding: 12px 30px;
                    border-radius: 5px;
                    display: inline-block;
                    font-size: 16px;
                    font-weight: bold;
                    transition: background-color 0.3s;
                }}
                .button:hover {{
                    background-color: #2980b9;
                }}
                .info {{
                    background-color: #f8f9fa;
                    padding: 15px;
                    border-left: 4px solid #3498db;
                    margin: 20px 0;
                    font-size: 14px;
                    color: #666666;
                }}
                .footer {{
                    background-color: #f4f4f4;
                    padding: 20px;
                    text-align: center;
                    font-size: 12px;
                    color: #999999;
                    border-top: 1px solid #e0e0e0;
                }}
                .warning {{
                    color: #e74c3c;
                    font-size: 12px;
                    margin-top: 20px;
                }}
                @media only screen and (max-width: 600px) {{
                    .container {{
                        width: 100%;
                        margin: 0;
                        border-radius: 0;
                    }}
                    .content {{
                        padding: 30px 20px;
                    }}
                    .button {{
                        display: block;
                        text-align: center;
                    }}
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Lanchonete Simulator</h1>
                </div>
                
                <div class="content">
                    <div class="greeting">
                        Ola, <strong>{nome_usuario}</strong>!
                    </div>
                    
                    <div class="message">
                        Recebemos uma solicitacao de recuperacao de senha para sua conta no 
                        <strong>Lanchonete Simulator</strong>.
                    </div>
                    
                    <div class="button-container">
                        <a href="{link_recuperacao}" class="button">
                            Redefinir Minha Senha
                        </a>
                    </div>
                    
                    <div class="info">
                        <strong>Informacoes importantes:</strong><br>
                        - Este link e valido por {horas_validade} hora(s)<br>
                        - Apos esse periodo, sera necessario solicitar um novo link<br>
                        - O link leva para uma pagina segura do nosso sistema
                    </div>
                    
                    <div class="message">
                        Se o botao acima nao funcionar, copie e cole o link abaixo no seu navegador:
                        <br>
                        <small style="color: #3498db; word-break: break-all;">
                            {link_recuperacao}
                        </small>
                    </div>
                    
                    <div class="warning">
                        <strong>Atencao:</strong> Se voce nao solicitou essa alteracao, ignore este email.
                        Sua senha permanecera inalterada.
                    </div>
                </div>
                
                <div class="footer">
                    <p>Lanchonete Simulator - Sistema de Gestao</p>
                    <p>Este e um email automatico, por favor nao responda.</p>
                    <p>&copy; 2024 Lanchonete Simulator. Todos os direitos reservados.</p>
                </div>
            </div>
        </body>
        </html>
        """
        return html
    
    def _gerar_texto_alternativo(self, nome_usuario, link_recuperacao, horas_validade=1):
        """Gera versao em texto puro para clientes de email que nao suportam HTML"""
        texto = f"""
Lanchonete Simulator - Recuperacao de Senha

Ola {nome_usuario}!

Recebemos uma solicitacao de recuperacao de senha para sua conta.

Para redefinir sua senha, acesse o link abaixo:
{link_recuperacao}

Informacoes importantes:
- Este link e valido por {horas_validade} hora(s)
- Apos esse periodo, sera necessario solicitar um novo link

Se voce nao solicitou essa alteracao, ignore este email. Sua senha permanecera inalterada.

---
Lanchonete Simulator - Sistema de Gestao
Este e um email automatico, por favor nao responda.
"""
        return texto.strip()
    
    def enviar_email_recuperacao(self, email_destino, token, nome_usuario, horas_validade=1):
        """
        Envia email de recuperacao de senha
        Com validacoes de seguranca e sanitizacao
        """
        # ========== VALIDACOES DE SEGURANCA ==========
        
        # Validar email
        if not self._validar_email(email_destino):
            logger.error(f"Email invalido: {email_destino}")
            return False
        
        # Sanitizar entradas
        email_destino = self._sanitizar_input(email_destino)
        nome_usuario = self._sanitizar_input(nome_usuario)
        
        # Validar token (deve ser hexadecimal de 64 caracteres)
        if not token or len(token) != 64 or not all(c in '0123456789abcdef' for c in token.lower()):
            logger.error("Token invalido ou mal formatado")
            return False
        
        # ========== CONSTRUCAO SEGURA DO LINK ==========
        # Usar URL base de variavel de ambiente
        url_base = os.getenv('URL_BASE', 'https://localhost:5000')
        link_recuperacao = f"{url_base}/redefinir-senha?token={token}"
        
        # ========== CORPO DO EMAIL ==========
        html_email = self._gerar_html_email(nome_usuario, link_recuperacao, horas_validade)
        texto_alternativo = self._gerar_texto_alternativo(nome_usuario, link_recuperacao, horas_validade)
        
        # ========== MODO TESTE ==========
        if self.modo_teste:
            return self._simular_envio(email_destino, token, link_recuperacao, nome_usuario, html_email)
        
        # ========== MODO REAL ==========
        return self._enviar_email_real(email_destino, html_email, texto_alternativo, nome_usuario)
    
    def _simular_envio(self, email_destino, token, link_recuperacao, nome_usuario, html_email):
        """Simula envio de email no terminal (modo teste seguro)"""
        print("\n" + "=" * 70)
        print("SIMULACAO DE EMAIL DE RECUPERACAO DE SENHA")
        print("=" * 70)
        print(f"Para: {email_destino}")
        print(f"Usuario: {nome_usuario}")
        print(f"Token: {token[:10]}...{token[-10:]}")
        print(f"Link: {link_recuperacao}")
        print("-" * 70)
        print("HTML DO EMAIL (versao resumida):")
        print("-" * 70)
        # Mostra apenas parte do HTML para nao poluir o terminal
        print(html_email[:500] + "...")
        print("=" * 70)
        print("MODO TESTE ATIVO - Nenhum email foi enviado")
        print("Para enviar emails reais, configure o arquivo .env com:")
        print("  EMAIL_MODO_TESTE=False")
        print("  EMAIL_USER=seu-email@gmail.com")
        print("  EMAIL_PASSWORD=sua-senha")
        print("=" * 70 + "\n")
        
        # Log seguro
        logger.info(f"Simulacao de email para {email_destino[:3]}***")
        return True
    
    def _enviar_email_real(self, email_destino, html_email, texto_alternativo, nome_usuario):
        """
        Envia email real via SMTP com tratamento de erros
        e configuracoes seguras
        """
        try:
            # Criar mensagem com MIMEMultipart para suporte a HTML
            msg = MIMEMultipart('alternative')
            msg['Subject'] = 'Recuperacao de senha - Lanchonete Simulator'
            msg['From'] = self.email_from
            msg['To'] = email_destino
            msg['Reply-To'] = self.email_from
            
            # Adicionar cabecalhos de seguranca
            msg['X-Priority'] = '3'
            msg['X-Mailer'] = 'Lanchonete-Simulator/1.0'
            msg['X-Originating-IP'] = '127.0.0.1'
            
            # Anexar versao em texto puro e HTML
            part_text = MIMEText(texto_alternativo, 'plain', 'utf-8')
            part_html = MIMEText(html_email, 'html', 'utf-8')
            
            msg.attach(part_text)
            msg.attach(part_html)
            
            # Configurar conexao segura
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                # Timeout para evitar ataques de negacao de servico
                server.timeout = 30
                
                # Iniciar TLS (criptografia)
                server.starttls()
                
                # Autenticacao (com timeout)
                server.login(self.email_user, self.email_password)
                
                # Enviar email (com timeout)
                server.send_message(msg)
            
            # Log seguro (sem expor dados sensiveis)
            logger.info(f"Email de recuperacao enviado para {email_destino[:3]}***")
            return True
            
        except smtplib.SMTPAuthenticationError:
            logger.error("Falha na autenticacao SMTP - Verifique usuario/senha")
            return False
        except smtplib.SMTPException as e:
            logger.error(f"Erro SMTP ao enviar email: {type(e).__name__}")
            return False
        except Exception as e:
            logger.error(f"Erro inesperado ao enviar email: {type(e).__name__}")
            return False
    
    def testar_conexao_smtp(self):
        """Metodo para testar a conexao SMTP sem enviar email"""
        if self.modo_teste:
            print("Modo teste ativo - Nao e possivel testar SMTP real")
            return False
        
        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.timeout = 10
                server.starttls()
                server.login(self.email_user, self.email_password)
                print("Conexao SMTP bem-sucedida!")
                return True
        except Exception as e:
            print(f"Falha na conexao SMTP: {e}")
            return False


# ========== INSTANCIACAO SEGURA ==========
try:
    email_utils = EmailUtils()
    logger.info("EmailUtils inicializado com sucesso")
except ValueError as e:
    logger.error(f"Erro na inicializacao: {e}")
    # Criar instancia em modo teste como fallback
    email_utils = EmailUtils()
    email_utils.modo_teste = True
    logger.warning("EmailUtils rodando em modo teste por seguranca")