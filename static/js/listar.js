window.deletarPedido = function(id) {
    ModalSystem.confirm('Tem certeza que deseja deletar este pedido?', function() {
        LoadingSystem.show();
        
        fetch('/pedidos/' + id, {
            method: 'DELETE'
        })
        .then(function(response) {
            return response.json();
        })
        .then(function(result) {
            if (result.success) {
                var row = document.getElementById('pedido-' + id);
                if (row) {
                    row.remove();
                    NotificationSystem.show(result.message, 'success');
                    
                    var remainingRows = document.querySelectorAll('#pedidos-table tbody tr').length;
                    if (remainingRows === 0) {
                        setTimeout(function() {
                            location.reload();
                        }, 500);
                    }
                }
            } else {
                NotificationSystem.show(result.message, 'error');
            }
            LoadingSystem.hide();
        })
        .catch(function(error) {
            NotificationSystem.show('Erro ao deletar pedido', 'error');
            LoadingSystem.hide();
        });
    });
};