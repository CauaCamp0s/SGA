CREATE DATABASE associacao;
USE associacao;

CREATE TABLE Associados (
    associado_id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(255) NOT NULL,
    endereco VARCHAR(255),
    email VARCHAR(255) NOT NULL,
    telefone VARCHAR(20),
    tipo_associado VARCHAR(50),
    data_inicio_associacao DATE,
    data_fim_associacao DATE
);


CREATE TABLE Eventos (
    evento_id INT PRIMARY KEY AUTO_INCREMENT,
    nome_evento VARCHAR(255) NOT NULL,
    data_evento DATE,
    descricao TEXT,
    localizacao VARCHAR(255)
);

CREATE TABLE Pagamentos (
    pagamento_id INT PRIMARY KEY AUTO_INCREMENT,
    associado_id INT,
    data_pagamento DATE,
    valor DECIMAL(10, 2),
    tipo_pagamento VARCHAR(50),
    FOREIGN KEY (associado_id) REFERENCES Associados(associado_id)
);

CREATE TABLE CadastroAssociados (
    associado_id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(255) NOT NULL,
    endereco VARCHAR(255),
    cidade VARCHAR(100),
    estado VARCHAR(50),
    cep VARCHAR(10),
    email VARCHAR(255) UNIQUE,
    telefone VARCHAR(20),
    tipo_associado ENUM('Regular', 'Premium') DEFAULT 'Regular',
    data_inicio_associacao DATE,
    data_fim_associacao DATE,
    ativo BOOLEAN DEFAULT TRUE
);


CREATE TABLE Users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);



GRANT ALL PRIVILEGES ON associacao.* TO 'root'@'localhost';


-- Inserir um associado na tabela 'Associados'
INSERT INTO Associados (nome, endereco, email, telefone, tipo_associado, data_inicio_associacao, data_fim_associacao)
VALUES ('João Silva', 'Rua A, 123', 'joao@example.com', '123456789', 'Premium', '2024-05-01', '2025-05-01');

-- Inserir um evento na tabela 'Eventos'
INSERT INTO Eventos (nome_evento, data_evento, descricao, localizacao)
VALUES ('Conferência Anual', '2024-06-15', 'Uma conferência sobre tecnologia', 'Centro de Convenções');

-- Inserir um pagamento na tabela 'Pagamentos'
-- Comando SQL para inserir pagamentos associados ao ID 1 (João Silva)
INSERT INTO Pagamentos (associado_id, data_pagamento, valor, tipo_pagamento)
VALUES (1, '2024-05-10', 100.00, 'Cartão de Crédito');

-- Comando SQL para inserir pagamentos associados ao ID 2 (João Silva)
INSERT INTO Pagamentos (associado_id, data_pagamento, valor, tipo_pagamento)
VALUES (2, '2024-05-15', 80.00, 'Boleto Bancário');

-- Comando SQL para inserir pagamentos associados ao ID 3 (Maria Oliveira)
INSERT INTO Pagamentos (associado_id, data_pagamento, valor, tipo_pagamento)
VALUES (3, '2024-05-20', 120.00, 'Transferência Bancária');

-- Comando SQL para inserir pagamentos associados ao ID 4 (Maria Oliveira)
INSERT INTO Pagamentos (associado_id, data_pagamento, valor, tipo_pagamento)
VALUES (4, '2024-05-25', 90.00, 'Cartão de Débito');

-- Comando SQL para inserir pagamentos associados ao ID 5 (caua)
INSERT INTO Pagamentos (associado_id, data_pagamento, valor, tipo_pagamento)
VALUES (5, '2024-06-01', 150.00, 'Pix');

