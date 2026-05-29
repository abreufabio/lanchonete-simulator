
CREATE DATABASE IF NOT EXISTS lanchonete;
USE lanchonete;

CREATE TABLE IF NOT EXISTS pedidos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cliente VARCHAR(100) NOT NULL,
    lanche VARCHAR(100) NOT NULL,
    quantidade INT NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'Pendente'
);

INSERT INTO pedidos (cliente, lanche, quantidade, status) VALUES
('João Silva', 'X-Burger', 2, 'Pendente'),
('Maria Santos', 'X-Salada', 1, 'Preparando'),
('Pedro Oliveira', 'X-Tudo', 3, 'Pronto'),
('Ana Costa', 'Hot Dog', 2, 'Entregue');
