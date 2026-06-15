// Login JavaScript - Integração com Flask backend
class LoginManager {
    constructor() {
        this.form = document.getElementById('loginForm');
        this.emailInput = document.getElementById('email');
        this.passwordInput = document.getElementById('password');
        this.loginBtn = document.getElementById('loginBtn');
        this.registerBtn = document.getElementById('registerBtn');
        this.notification = document.getElementById('notification');
        this.modal = document.getElementById('registerModal');
        
        this.init();
    }
    
    init() {
        // NÃO preencher campos automaticamente
        // Limpar quaisquer valores que possam ter sido salvos pelo navegador
        if (this.emailInput) {
            this.emailInput.value = '';
        }
        if (this.passwordInput) {
            this.passwordInput.value = '';
        }
        
        if (this.form) {
            this.form.addEventListener('submit', (e) => this.handleLogin(e));
        }
        
        if (this.registerBtn) {
            this.registerBtn.addEventListener('click', () => this.openRegisterModal());
        }
        
        const closeBtn = document.querySelector('.close');
        if (closeBtn) {
            closeBtn.addEventListener('click', () => this.closeRegisterModal());
        }
        
        window.addEventListener('click', (e) => {
            if (e.target === this.modal) {
                this.closeRegisterModal();
            }
        });
        
        const registerForm = document.getElementById('registerForm');
        if (registerForm) {
            registerForm.addEventListener('submit', (e) => this.handleRegister(e));
        }
        
        //Verifica o link de recupeçaão de senha
        const forgotLink = document.getElementById('forgotLink');
        if (forgotLink) {
            forgotLink.addEventListener('click', (e) => {
                window.location.href = '/recuperar-senha';
            });
        }
        
        // Verificar sessão apenas se não estiver na página de login
        this.checkSession();
    }
    
    showNotification(message, type = 'success') {
        if (!this.notification) return;
        
        this.notification.textContent = message;
        this.notification.className = `notification ${type}`;
        this.notification.classList.add('show');
        
        setTimeout(() => {
            this.notification.classList.remove('show');
        }, 3000);
    }
    
    setLoading(isLoading) {
        if (!this.loginBtn) return;
        
        if (isLoading) {
            this.loginBtn.disabled = true;
            const originalText = this.loginBtn.innerHTML;
            this.loginBtn.dataset.originalText = originalText;
            this.loginBtn.innerHTML = '<span class="spinner"></span><span> Entrando...</span>';
        } else {
            this.loginBtn.disabled = false;
            if (this.loginBtn.dataset.originalText) {
                this.loginBtn.innerHTML = this.loginBtn.dataset.originalText;
            }
        }
    }
    
    setRegisterLoading(isLoading) {
        const registerSubmitBtn = document.querySelector('#registerForm button[type="submit"]');
        if (!registerSubmitBtn) return;
        
        if (isLoading) {
            registerSubmitBtn.disabled = true;
            registerSubmitBtn.innerHTML = '<span class="spinner"></span> Cadastrando...';
        } else {
            registerSubmitBtn.disabled = false;
            registerSubmitBtn.innerHTML = 'Cadastrar';
        }
    }
    
    async handleLogin(event) {
        event.preventDefault();
        
        const email = this.emailInput?.value.trim();
        const password = this.passwordInput?.value;
        
        if (!email || !password) {
            this.showNotification('Por favor, preencha email e senha.', 'error');
            return;
        }
        
        if (!this.validateEmail(email)) {
            this.showNotification('Por favor, insira um email válido.', 'error');
            return;
        }
        
        this.setLoading(true);
        
        try {
            const response = await fetch('/api/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email, password })
            });
            
            const data = await response.json();
            
            if (response.ok && data.success) {
                this.showNotification('✅ Login realizado com sucesso! Redirecionando...', 'success');
                
                setTimeout(() => {
                    window.location.href = data.redirect_url || '/pedidos';
                }, 1500);
            } else {
                this.showNotification(data.message || '❌ Email ou senha inválidos.', 'error');
                this.setLoading(false);
                if (this.passwordInput) this.passwordInput.value = '';
                if (this.emailInput) this.emailInput.focus();
            }
        } catch (error) {
            console.error('Erro no login:', error);
            this.showNotification('Erro de conexão. Tente novamente mais tarde.', 'error');
            this.setLoading(false);
        }
    }
    
    openRegisterModal() {
        if (this.modal) {
            // Limpar formulário do modal
            const registerForm = document.getElementById('registerForm');
            if (registerForm) {
                registerForm.reset();
            }
            this.modal.style.display = 'block';
            // Impedir scroll do body quando modal está aberto
            document.body.style.overflow = 'hidden';
        }
    }
    
    closeRegisterModal() {
        if (this.modal) {
            this.modal.style.display = 'none';
            document.body.style.overflow = 'auto';
        }
    }
    
    async handleRegister(event) {
        event.preventDefault();
        
        const nome = document.getElementById('regNome')?.value.trim();
        const email = document.getElementById('regEmail')?.value.trim();
        const senha = document.getElementById('regSenha')?.value;
        const confirmSenha = document.getElementById('regConfirmSenha')?.value;
        
        if (!nome || !email || !senha) {
            this.showNotification('Por favor, preencha todos os campos.', 'error');
            return;
        }
        
        if (nome.length < 3) {
            this.showNotification('Nome deve ter pelo menos 3 caracteres.', 'error');
            return;
        }
        
        if (!this.validateEmail(email)) {
            this.showNotification('Por favor, insira um email válido.', 'error');
            return;
        }
        
        if (senha.length < 6) {
            this.showNotification('A senha deve ter pelo menos 6 caracteres.', 'error');
            return;
        }
        
        if (senha !== confirmSenha) {
            this.showNotification('As senhas não conferem.', 'error');
            return;
        }
        
        this.setRegisterLoading(true);
        
        try {
            const response = await fetch('/api/registrar', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ nome, email, senha })
            });
            
            const data = await response.json();
            
            if (response.ok && data.success) {
                this.showNotification('✅ Cadastro realizado com sucesso! Faça login.', 'success');
                this.closeRegisterModal();
                
                // Preencher apenas o email no formulário de login
                if (this.emailInput) {
                    this.emailInput.value = email;
                    this.emailInput.focus();
                }
                if (this.passwordInput) {
                    this.passwordInput.value = '';
                }
            } else {
                this.showNotification(data.message || '❌ Erro ao cadastrar.', 'error');
            }
        } catch (error) {
            console.error('Erro no cadastro:', error);
            this.showNotification('Erro de conexão. Tente novamente.', 'error');
        } finally {
            this.setRegisterLoading(false);
        }
    }
    
    validateEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    }
    
    async checkSession() {
        try {
            const response = await fetch('/api/check-session');
            const data = await response.json();
            
            if (data.logged_in) {
                window.location.href = '/pedidos';
            }
        } catch (error) {
            console.error('Erro ao verificar sessão:', error);
        }
    }
}

// Inicializar quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', () => {
    new LoginManager();
});