CREATE DATABASE associacao;
USE associacao;

CREATE TABLE `associados` (
  `associado_id` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(255) NOT NULL,
  `endereco` varchar(255) DEFAULT NULL,
  `email` varchar(255) NOT NULL,
  `telefone` varchar(20) DEFAULT NULL,
  `tipo_associado` varchar(50) DEFAULT NULL,
  `data_inicio_associacao` date DEFAULT NULL,
  `data_fim_associacao` date DEFAULT NULL,
  `cpf_cnpj` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`associado_id`)
);

CREATE TABLE `cadastroassociados` (
  `associado_id` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(255) NOT NULL,
  `endereco` varchar(255) DEFAULT NULL,
  `cidade` varchar(100) DEFAULT NULL,
  `estado` varchar(50) DEFAULT NULL,
  `cep` varchar(10) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `telefone` varchar(20) DEFAULT NULL,
  `tipo_associado` enum('Regular','Premium') DEFAULT 'Regular',
  `data_inicio_associacao` date DEFAULT NULL,
  `data_fim_associacao` date DEFAULT NULL,
  `ativo` tinyint(1) DEFAULT '1',
  `cpf_cnpj` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`associado_id`),
  UNIQUE KEY `email` (`email`)
);

CREATE TABLE `eventos` (
  `evento_id` int NOT NULL AUTO_INCREMENT,
  `nome_evento` varchar(255) NOT NULL,
  `data_evento` date DEFAULT NULL,
  `descricao` text,
  `localizacao` varchar(255) DEFAULT NULL,
  `associado_id` int DEFAULT NULL,
  PRIMARY KEY (`evento_id`),
  KEY `fk_associado_id` (`associado_id`),
  CONSTRAINT `eventos_ibfk_1` FOREIGN KEY (`associado_id`) REFERENCES `associados` (`associado_id`),
  CONSTRAINT `fk_associado_id` FOREIGN KEY (`associado_id`) REFERENCES `associados` (`associado_id`)
);

CREATE TABLE `pagamentos` (
  `pagamento_id` int NOT NULL AUTO_INCREMENT,
  `associado_id` int DEFAULT NULL,
  `data_pagamento` date DEFAULT NULL,
  `valor` decimal(10,2) DEFAULT NULL,
  `tipo_pagamento` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`pagamento_id`),
  KEY `associado_id` (`associado_id`),
  CONSTRAINT `pagamentos_ibfk_1` FOREIGN KEY (`associado_id`) REFERENCES `associados` (`associado_id`)
);

CREATE TABLE `users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `email` (`email`)
);