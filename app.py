from flask import Flask, render_template, request, url_for, redirect, jsonify  # CORRIGIDO: Flask com F maiúsculo
from models.pedido import Pedido

app = Flask(__name__)
pedido_model = Pedido()

@app.route('/')  # CORRIGIDO: routa para route
def index():
    return redirect(url_for('listar_pedidos'))

# rota para ir para listagem de pedidos
@app.route('/pedidos', methods=['GET'])
def listar_pedidos():
    pedidos = pedido_model.listar_todos()
    return render_template('listar.html', pedidos=pedidos)

# rota para ir para pagina de cadastro de pedidos
@app.route('/pedidos/cadastrar', methods=['GET'])
def pagina_cadastrar():
    return render_template('cadastrar.html')

# Metodo Post para cadastrar um pedido
@app.route('/pedidos', methods=['POST'])
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

# Rota para ir para a pagina de edição
@app.route('/pedidos/editar/<int:pedido_id>', methods=['GET'])
def pagina_editar(pedido_id):
    pedido = pedido_model.buscar_por_id(pedido_id)
    if pedido:
        return render_template('editar.html', pedido=pedido)
    else:
        return redirect(url_for('listar_pedidos'))

# Rota para editar um pedido - método PUT
@app.route('/pedidos/<int:pedido_id>', methods=['PUT'])
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

# Rota para deletar um pedido - método DELETE
@app.route('/pedidos/<int:pedido_id>', methods=['DELETE'])
def deletar_pedido(pedido_id):
    try:
        if pedido_model.deletar(pedido_id):
            return jsonify({'success': True, 'message': 'Pedido deletado com sucesso!'}), 200
        else:
            return jsonify({'success': False, 'message': 'Erro ao deletar pedido'}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

# Rota para página de alterar status
@app.route('/pedidos/status/<int:pedido_id>', methods=['GET'])
def pagina_alterar_status(pedido_id):
    pedido = pedido_model.buscar_por_id(pedido_id)
    if pedido:
        return render_template('alterar_status.html', pedido=pedido)
    return redirect(url_for('listar_pedidos'))

# Rota para alterar o status - método PUT
@app.route('/pedidos/status/<int:pedido_id>', methods=['PUT'])
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