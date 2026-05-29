var NotificationSystem = {
    show: function(message, type) {
        var notification = document.createElement('div');
        notification.className = 'notification ' + type;
        
        var icon = this.getIcon(type);
        notification.innerHTML = icon + '<span>' + message + '</span>';
        
        document.body.appendChild(notification);
        
        setTimeout(function() {
            notification.style.animation = 'fadeOut 0.3s ease forwards';
            setTimeout(function() {
                notification.remove();
            }, 300);
        }, 3000);
    },
    
    getIcon: function(type) {
        var icons = {
            success: '<span style="font-size: 18px; font-weight: bold;">✓</span>',
            error: '<span style="font-size: 18px; font-weight: bold;">✗</span>',
            warning: '<span style="font-size: 18px; font-weight: bold;">⚠</span>',
            info: '<span style="font-size: 18px; font-weight: bold;">ℹ</span>'
        };
        return icons[type] || icons.info;
    }
};

var ModalSystem = {
    show: function(title, content, onConfirm, onCancel) {
        var modal = document.createElement('div');
        modal.className = 'modal';
        modal.innerHTML = `
            <div class="modal-content">
                <div class="modal-header">
                    <span class="close-modal">&times;</span>
                    <h3>${title}</h3>
                </div>
                <div class="modal-body">
                    ${content}
                </div>
                <div class="modal-footer">
                    <button class="btn btn-cancel" id="modalCancel">Cancelar</button>
                    <button class="btn btn-primary" id="modalConfirm">Confirmar</button>
                </div>
            </div>
        `;
        
        document.body.appendChild(modal);
        modal.style.display = 'block';
        
        var closeModal = function() {
            modal.remove();
        };
        
        modal.querySelector('.close-modal').onclick = function() {
            if (onCancel) onCancel();
            closeModal();
        };
        
        modal.querySelector('#modalCancel').onclick = function() {
            if (onCancel) onCancel();
            closeModal();
        };
        
        modal.querySelector('#modalConfirm').onclick = function() {
            if (onConfirm) onConfirm();
            closeModal();
        };
        
        modal.onclick = function(e) {
            if (e.target === modal) {
                if (onCancel) onCancel();
                closeModal();
            }
        };
        
        return modal;
    },
    
    confirm: function(message, onConfirm) {
        this.show('Confirmacao', '<p>' + message + '</p>', onConfirm);
    }
};

var LoadingSystem = {
    show: function() {
        var loader = document.createElement('div');
        loader.className = 'modal';
        loader.id = 'globalLoader';
        loader.style.backgroundColor = 'rgba(0, 0, 0, 0.5)';
        loader.innerHTML = '<div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);"><div class="loader" style="width: 50px; height: 50px;"></div></div>';
        document.body.appendChild(loader);
        loader.style.display = 'block';
    },
    
    hide: function() {
        var loader = document.getElementById('globalLoader');
        if (loader) loader.remove();
    }
};