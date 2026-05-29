document.addEventListener('DOMContentLoaded', function() {
    var form = document.getElementById('statusForm');
    
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            LoadingSystem.show();
            
            var pedidoId = document.getElementById('pedido_id').value;
            var data = {
                status: document.getElementById('status').value
            };
            
            fetch('/pedidos/status/' + pedidoId, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            })
            .then(function(response) {
                return response.json();
            })
            .then(function(result) {
                if (result.success) {
                    NotificationSystem.show(result.message, 'success');
                    setTimeout(function() {
                        window.location.href = '/pedidos';
                    }, 1500);
                } else {
                    NotificationSystem.show(result.message, 'error');
                }
                LoadingSystem.hide();
            })
            .catch(function(error) {
                NotificationSystem.show('Erro ao alterar status', 'error');
                LoadingSystem.hide();
            });
        });
    }
});