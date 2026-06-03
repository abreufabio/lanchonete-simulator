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