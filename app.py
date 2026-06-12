from flask import Flask, render_template, request, url_for, redirect, jsonify, session
from functools import wraps
from models.pedido import Pedido
from models.usuario import Usuario
from database import init_database

app = Flask(__name__)
app.secret_key = 'Cauã_é_uma_besta'

# Inicializar banco de dados
init_database()

pedido_model = Pedido()

# Decorator de autenticação
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Rotas de autenticação
@app.route('/login', methods=['GET'])
def login():
    if 'user_id' in session:
        return redirect(url_for('listar_pedidos'))
    return render_template('login.html')

@app.route('/api/login', methods=['POST'])
def api_login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({'success': False, 'message': 'Email e senha são obrigatórios'}), 400
        
        usuario = Usuario.autenticar(email, password)
        
        if usuario:
            session['user_id'] = usuario.id
            session['user_nome'] = usuario.nome
            session['user_email'] = usuario.email
            
            return jsonify({
                'success': True,
                'message': 'Login realizado com sucesso',
                'redirect_url': '/pedidos',
                'user': usuario.to_dict()
            })
        else:
            return jsonify({'success': False, 'message': 'Email ou senha inválidos'}), 401
            
    except Exception as e:
        print(f"Erro no login: {e}")
        return jsonify({'success': False, 'message': 'Erro interno do servidor'}), 500

@app.route('/api/registrar', methods=['POST'])
def api_registrar():
    try:
        data = request.get_json()
        nome = data.get('nome')
        email = data.get('email')
        senha = data.get('senha')
        
        if not nome or not email or not senha:
            return jsonify({'success': False, 'message': 'Todos os campos são obrigatórios'}), 400
        
        if len(nome) < 3:
            return jsonify({'success': False, 'message': 'Nome deve ter pelo menos 3 caracteres'}), 400
        
        if len(senha) < 6:
            return jsonify({'success': False, 'message': 'Senha deve ter pelo menos 6 caracteres'}), 400
        
        sucesso, mensagem = Usuario.cadastrar(nome, email, senha)
        
        if sucesso:
            return jsonify({
                'success': True,
                'message': 'Cadastro realizado com sucesso! Faça login.'
            })
        else:
            return jsonify({'success': False, 'message': mensagem}), 400
            
    except Exception as e:
        print(f"Erro no cadastro: {e}")
        return jsonify({'success': False, 'message': 'Erro interno do servidor'}), 500

@app.route('/api/check-session', methods=['GET'])
def check_session():
    if 'user_id' in session:
        return jsonify({
            'logged_in': True, 
            'user': {
                'nome': session.get('user_nome'),
                'email': session.get('user_email')
            }
        })
    return jsonify({'logged_in': False})

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('login'))

# Rotas do sistema (protegidas)
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('listar_pedidos'))
    return redirect(url_for('login'))

@app.route('/pedidos', methods=['GET'])
@login_required
def listar_pedidos():
    pedidos = pedido_model.listar_todos()
    return render_template('listar.html', pedidos=pedidos, usuario=session.get('user_nome'))

@app.route('/pedidos/cadastrar', methods=['GET'])
@login_required
def pagina_cadastrar():
    return render_template('cadastrar.html', usuario=session.get('user_nome'))

@app.route('/pedidos', methods=['POST'])
@login_required
def cadastrar_pedido():
    try:
        cliente = request.form.get('cliente')
        lanche = request.form.get('lanche')
        quantidade = int(request.form.get('quantidade'))
        status = request.form.get('status')
        
        if pedido_model.cadastrar(cliente, lanche, quantidade, status):
            return jsonify({'success': True, 'message': 'Pedido cadastrado com sucesso!'}), 201
        else:
            return jsonify({'success': False, 'message': 'Erro ao cadastrar pedido'}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/pedidos/editar/<int:pedido_id>', methods=['GET'])
@login_required
def pagina_editar(pedido_id):
    pedido = pedido_model.buscar_por_id(pedido_id)
    if pedido:
        return render_template('editar.html', pedido=pedido, usuario=session.get('user_nome'))
    else:
        return redirect(url_for('listar_pedidos'))

@app.route('/pedidos/<int:pedido_id>', methods=['PUT'])
@login_required
def editar_pedido(pedido_id):
    try:
        data = request.get_json()
        cliente = data.get('cliente')
        lanche = data.get('lanche')
        quantidade = int(data.get('quantidade'))
        status = data.get('status')
        
        if pedido_model.editar(pedido_id, cliente, lanche, quantidade, status):
            return jsonify({'success': True, 'message': 'Pedido editado com sucesso!'}), 200
        else:
            return jsonify({'success': False, 'message': 'Erro ao editar pedido'}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/pedidos/<int:pedido_id>', methods=['DELETE'])
@login_required
def deletar_pedido(pedido_id):
    try:
        if pedido_model.deletar(pedido_id):
            return jsonify({'success': True, 'message': 'Pedido deletado com sucesso!'}), 200
        else:
            return jsonify({'success': False, 'message': 'Erro ao deletar pedido'}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/pedidos/status/<int:pedido_id>', methods=['GET'])
@login_required
def pagina_alterar_status(pedido_id):
    pedido = pedido_model.buscar_por_id(pedido_id)
    if pedido:
        return render_template('alterar_status.html', pedido=pedido, usuario=session.get('user_nome'))
    return redirect(url_for('listar_pedidos'))

@app.route('/pedidos/status/<int:pedido_id>', methods=['PUT'])
@login_required
def alterar_status_pedido(pedido_id):
    try:
        data = request.get_json()
        novo_status = data.get('status')
        
        if pedido_model.alterar_status(pedido_id, novo_status):
            return jsonify({'success': True, 'message': 'Status do pedido alterado com sucesso!'}), 200
        else:
            return jsonify({'success': False, 'message': 'Erro ao alterar status do pedido'}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)

# =========== ROTAS PARA ALTERAR A SENHA DO USUARIO ====================
@app.route('/alterar-senha', methods=['GET'])
@login_required
def pagina_alterar_senha():
    return render_template('alterar_senha.html', usuario=session.get('user_nome'))

@app.route('/api/alterar-senha', methods=['POST'])
@login_required
def api_alterar_senha():
    try:
        data = request.get_json()
        senha_atual = data.get('senha_atual')
        nova_senha = data.get('nova_senha')

        if not senha_atual or not nova_senha:
            return jsonify({'success': False, 'message': 'Todos os campos são obrigatórios'}), 400

        # =========== Verifcação de senha atual
        usuario = Usuario.autenticar(session['user_email'], senha_atual)
        if not usuario:
            return jsonify({'success': False, 'message': 'Senha atual incorreta'}), 400
        
        # ========== Validação da senha forte
        from database import db_instance
        valida, msg = db_instance.validar_senha_forte(nova_senha)
        if not valida:
            return jsonify({'success': False, 'message': msg}), 400
        
        # ========== Atualizar senha
        sucesso, mensagem = db_instance.atualizar_senha(session['user_id'], nova_senha)
        if sucesso:
            return jsonify({'success': True, 'message': mensagem})
        return jsonify({'success': False, 'message': mensagem}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# ====================== ROTAS DE RECUPEÇÃO SENHA ====================
@app.route('/recuperar-senha', methods=['GET'])
def pagina_recuperar_senha():
    return render_template('recuperar_senha.html')

@app.route('/api/recuperar-senha', methods=['POST'])
def api_recuperar_senha():
    try:
        data = request.get_json()
        email = data.get('email')

        if not email or not email.strip():
            return jsonify({'success': False, 'message': 'Email é obrigatorio'}), 400
        from database import db_instance
        usuario = db_instance.buscar_usuario_por_email(email)

        # ======= Por segurança, vai retornar sempre sucesso
        if not usuario:
            return jsonify({'success': True, 'message': 'Se houver cadastro em nosso sistema receberá um email com as instruções'})
        
        # ======= Criação de email de recuperação. 
        from models.token_recuperacao import TokenRecuperacao
        token = TokenRecuperacao.criar_token(usuario['id'])

        if token:
            from utils.email_utils import email_utils
            email_utils.enviar_email_recuperacao(email, token, usuario['nome'])
            return jsonify({'success': True, 'message': 'Email de recuperação enviado para seu email'})
        
        return jsonify({'success': False, 'message': 'Erro ao gerar token'})
    except Exception as e:
        print(f"Erro: {e}")
        return jsonify({'success': False, 'messagem': 'Erro interno' }), 500

@app.route('/redefinir-senha', methods=['GET'])
def pagina_redefinir_senha():
    token = request.args.get('token')
    return render_template('redefinir_senha.html', token=token)

@app.route('/api/redefinir-senha', methods=['POST'])
def api_redefinir_senha():
    try: 
        data = request.get_json()
        token = data.get('token')
        nova_senha = data.get('nova_senha')

        if not token or not nova_senha:
            return  jsonify({'success': False, 'message': 'Token e nova senha são obrigatórios'}), 400
        from models.token_recuperacao import TokenRecuperacao
        from database import db_instance

        # ========= Validação de Token
        token_data = TokenRecuperacao.validar_token(token)
        if not token_data:
            return jsonify({'success': False, 'message': 'Token invalido ou expirado'}), 400
        
        # ========= Validação de senha forte
        valida, msg = db_instance.validar_senha_forte(nova_senha)
        if not valida:
            return jsonify({'success': False, 'message': msg}), 400
        
        # ========= Atualizar senha
        sucesso, mensagem = db_instance.atualizar_senha(token_data['usuario_id'], nova_senha)
        if sucesso: 
            TokenRecuperacao.usar_token(token)
            return jsonify({'success': True, 'message': 'Senha redefinida com sucesso!'})
        return jsonify({'success': False, 'message': mensagem}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500