CREATE DATABASE sgb;
use sgb;

CREATE TABLE `autor` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nome` text NOT NULL,
  PRIMARY KEY (`id`)
);

CREATE TABLE `emprestimo` (
  `id` int NOT NULL,
  `livro_id` int NOT NULL,
  `membro_id` int NOT NULL,
  `data_emprestimo` date NOT NULL,
  `data_devolucao` date DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `membro_id` (`membro_id`),
  KEY `fk_livro_id` (`livro_id`),
  CONSTRAINT `emprestimo_ibfk_2` FOREIGN KEY (`membro_id`) REFERENCES `membro` (`id`),
  CONSTRAINT `fk_livro_id` FOREIGN KEY (`livro_id`) REFERENCES `livro` (`id`)
) ;

CREATE TABLE `livro` (
  `id` int NOT NULL AUTO_INCREMENT,
  `titulo` text NOT NULL,
  `autor_id` int NOT NULL,
  `ano_publicacao` int DEFAULT NULL,
  `genero` text,
  `disponivel` int DEFAULT '1',
  PRIMARY KEY (`id`),
  KEY `autor_id` (`autor_id`),
  CONSTRAINT `livro_ibfk_1` FOREIGN KEY (`autor_id`) REFERENCES `autor` (`id`)
);

CREATE TABLE `membro` (
  `id` int NOT NULL,
  `nome` text NOT NULL,
  `email` text,
  `telefone` text,
  PRIMARY KEY (`id`)
) 