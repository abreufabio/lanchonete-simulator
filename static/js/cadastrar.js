document.addEventListener('DOMContentLoaded', function() {
    var form = document.getElementById('cadastroForm');
    
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            LoadingSystem.show();
            
            var formData = new FormData(e.target);
            
            fetch('/pedidos', {
                method: 'POST',
                body: formData
            })
            .then(function(response) {
                return response.json();
            })
            .then(function(result) {
                if (result.success) {
                    NotificationSystem.show(result.message, 'success');
                    e.target.reset();
                    
                    setTimeout(function() {
                        window.location.href = '/pedidos';
                    }, 1500);
                } else {
                    NotificationSystem.show(result.message, 'error');
                }
                LoadingSystem.hide();
            })
            .catch(function(error) {
                NotificationSystem.show('Erro ao cadastrar pedido', 'error');
                LoadingSystem.hide();
            });
        });
    }
});