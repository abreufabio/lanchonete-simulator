// Funções globais
window.deletarPedido = async function(id) {
    if (confirm('Tem certeza que deseja deletar este pedido?')) {
        try {
            const response = await fetch(`/pedidos/${id}`, {
                method: 'DELETE'
            });
            
            const result = await response.json();
            
            if (result.success) {
                const row = document.getElementById(`pedido-${id}`);
                if (row) row.remove();
                alert(result.message);
                
                // Recarregar a página se não houver mais pedidos
                const remainingRows = document.querySelectorAll('#pedidos-table tbody tr').length;
                if (remainingRows === 0) {
                    location.reload();
                }
            } else {
                alert('Erro: ' + result.message);
            }
        } catch (error) {
            alert('Erro ao deletar pedido');
        }
    }
};