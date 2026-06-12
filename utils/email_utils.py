class EmailUtils:
    def __init__(self):
        # ============ CONFIGURAR O STPM AQUI
        self.modo_teste = True #O true vai mostrar o token no terminal, mas o False irá enviar via email
    
    def enviar_email_recuperacao(self, email_destino, token, nome_usuario):
        # ========= ENVIA O EMAIL DE RECUPERAÇÃO DE SENHA
        link_recuperacao = f"http://localhost:5000/redefinir-senha?token={toen}"
        corpo_email = f"""
                    Olá {nome_usuario}! 
                    Segue link para recuperação de senha do
                    LANCHONETE SIMULATOR
                    {link_recuperacao}
                    Link valido por 1 (uma) hora

                    Caso não tenha solicitado ignore esse email.

                    -----
                    Lanchonte Simulator
                    """
        if self.modo_teste:
            #Para mostrar no terminal
            print("\n" + "=" * 60)
            print("SIMUNLAÇÃO DE EMAIL DE RECUPERAÇÃO")
            print("=" * 60)
            print(f"Para: {email_destino}")
            print(f"Token: {token}")
            print(f"Link: {link_recuperacao}")
            print("=" * 60)
            print("Configue o SMTP para envio real")
            print("=" * 60 + "\n")
            return True
        else:
            # ========== ENVIA O EMAIL REAL VIA PROTOCOLO STPM
            return self.enviar_email_real(email_destino, corpo_email)
    
    # ======== CONFIGURAÇÃO DE EMAIL VIA PROTOCOLO SMTP
    def enviar_email_real(self, email_destino, corpo):
        # Exemplo com o gmail
        import smtplib 
        from email.mime.text import MIMEText

        msg = MIMEText(corpo)
        msg['Subject'] = 'Recuperção de senha - Lanchonete Simulator'
        msg['From'] = 'testes.de.trabalhos.de.ti@gmail.com'
        msg['To'] = email_destino

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login('testes.de.trabalhos.de.ti@gmail.com', 'Pamonha1996@')
            server.send_message(msg)
        
        print(f"[EMAIL] Enviado para {email_destino}")
        return True


email_Utils = EmailUtils()
