DROP DATABASE IF EXISTS futebol_aula;
CREATE DATABASE IF NOT EXISTS futebol_aula ;
USE futebol_aula;
-- show databases;
-- describe ou desc funcionario;
-- show tables


-- Inicio da Execucao com usuario futebol
-- Remover tabelas do banco (ordem importa)
/*popular_torcedores
DROP TABLE Jogo;
DROP TABLE EquipeCampeonato;
DROP TABLE JogadorBrasileiro;
DROP TABLE JogadorEstrangeiro;
DROP TABLE Cidade;
DROP TABLE PaisesTecnicos;
DROP TABLE Tecnico;
DROP TABLE Campeonato;
DROP TABLE Equipe;
ALTER TABLE SeqEquipe AUTO_INCREMENT = 1;
ALTER TABLE SeqCampeonato AUTO_INCREMENT = 1;
*/
CREATE TABLE Equipe (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nome VARCHAR(32)
);

INSERT INTO Equipe (id, nome) VALUES (1, 'Palmeiras');
INSERT INTO Equipe (id, nome) VALUES (2, 'Santos');
INSERT INTO Equipe (id, nome) VALUES (3, 'SCCP');
INSERT INTO Equipe (id, nome) VALUES (4, 'SPFC');

CREATE TABLE Campeonato (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nome VARCHAR(32)
);

INSERT INTO Campeonato (id, nome) VALUES (1, 'Campeonato Brasileiro');
INSERT INTO Campeonato (id, nome) VALUES (2, 'Copa do Brasil');

CREATE TABLE JogadorBrasileiro (
  id INT AUTO_INCREMENT PRIMARY KEY,
  cpf VARCHAR(16) UNIQUE,
  nome VARCHAR(32),
  posicao VARCHAR(16),
  idEquipe INT,
  salario INT(9),
  CONSTRAINT fk_jogadorbrasileiro_idEquipe FOREIGN KEY(idEquipe)
    REFERENCES Equipe(id),
  CONSTRAINT ck_jogadorbrasileiro_posicao CHECK (posicao IN ('Goleiro', 'Lateral', 'Zagueiro', 'Meio-Campo', 'Atacante'))
);


INSERT INTO JogadorBrasileiro (cpf, nome, posicao, idEquipe, salario) 
  VALUES ('111.222.333.44', 'Sao Marcos', 'Goleiro', 1, 350000.75);
  select * from jogadorbrasileiro;
INSERT INTO JogadorBrasileiro (cpf, nome, posicao, idEquipe, salario) 
  VALUES ('098.765.345.12', 'Neymar', 'Atacante', 2, 565000.50);
INSERT INTO JogadorBrasileiro (cpf, nome, posicao, idEquipe, salario) 
  VALUES ('045.456.555.12', 'Betao', 'Zagueiro', 3, 18000.00);
INSERT INTO JogadorBrasileiro (cpf, nome, posicao, idEquipe, salario) 
  VALUES ('235.457.789-65', 'Alex', 'Meio-Campo', 1, 310000.20);
INSERT INTO JogadorBrasileiro (cpf, nome, posicao, idEquipe, salario) 
  VALUES ('777.854.123-68', 'Ronaldinho', 'Atacante', 2, 425000.00);
INSERT INTO JogadorBrasileiro (cpf, nome, posicao, idEquipe, salario) 
  VALUES ('159.487.236-00', 'Gilmar Fuba', 'Atacante', 3, 8500.00);
INSERT INTO JogadorBrasileiro (cpf, nome, posicao, idEquipe, salario) 
  VALUES ('457.148.230-00', 'Iranildo', 'Meio-Campo', null, 0);
INSERT INTO JogadorBrasileiro (cpf, nome, posicao, idEquipe, salario) 
  VALUES ('476.555.788-15', 'Odvan', 'Zagueiro', null, 0);



CREATE TABLE JogadorEstrangeiro (
  id INT AUTO_INCREMENT PRIMARY KEY,
  passaporte VARCHAR(16) UNIQUE,
  nome VARCHAR(32),
  posicao VARCHAR(16),
  idEquipe INT,
  paisOrigem VARCHAR(16),
  salario INT(9),
  CONSTRAINT fk_jogadorestrangeiro_idEquipe FOREIGN KEY(idEquipe)
    REFERENCES Equipe(id)
);

INSERT INTO JogadorEstrangeiro (passaporte, nome, posicao, idEquipe, paisOrigem, salario) 
  VALUES ('586.324.111.44', 'Arce', 'Lateral', 1, 'Paraguai', 200500.10);
INSERT INTO JogadorEstrangeiro (passaporte, nome, posicao, idEquipe, paisOrigem, salario) 
  VALUES ('348.562.363.14', 'Mancuso', 'Atacante', 3, 'Argentina', 110000.75);
INSERT INTO JogadorEstrangeiro (passaporte, nome, posicao, idEquipe, paisOrigem, salario) 
  VALUES ('456.357.698.47', 'Gioino', 'Atacante', 3, 'Argentina', 15000);


CREATE TABLE EquipeCampeonato (
  idEquipe INT,
  idCampeonato INT,
  posicao INT,
  PRIMARY KEY (idEquipe, idCampeonato),
  CONSTRAINT fk_equipecampeonato_idEquipe FOREIGN KEY (idEquipe)
    REFERENCES Equipe(id),
  CONSTRAINT fk_equipecampeonato_idCamp FOREIGN KEY (idCampeonato)
    REFERENCES Campeonato(id),
  CONSTRAINT ck_equipecampeonato_posicao CHECK (posicao > 0)
);

INSERT INTO EquipeCampeonato (idEquipe, idCampeonato, posicao)
  VALUES (1, 1, 1);
INSERT INTO EquipeCampeonato (idEquipe, idCampeonato, posicao)
  VALUES (2, 1, 16);
INSERT INTO EquipeCampeonato (idEquipe, idCampeonato, posicao)
  VALUES (3, 1, 3);
INSERT INTO EquipeCampeonato (idEquipe, idCampeonato, posicao)
  VALUES (4, 1, 8);

CREATE TABLE Cidade (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nome VARCHAR(32),
  estado VARCHAR(2)
);

INSERT INTO Cidade (id, nome, estado) VALUES (1, 'Sao Paulo', 'SP');
INSERT INTO Cidade (id, nome, estado) VALUES (2, 'Rio de Janeiro', 'RJ');
INSERT INTO Cidade (id, nome) VALUES ( 3, 'Belo Horizonte');
INSERT INTO Cidade (id, nome) VALUES (4, 'Porto Alegre');
INSERT INTO Cidade (id, nome) VALUES (5, 'Recife');

CREATE TABLE Tecnico (
  id INT AUTO_INCREMENT PRIMARY KEY,
  cpf VARCHAR(16) UNIQUE,
  nome VARCHAR(32),
  idEquipe INT,
  dataNasc DATE,
  CONSTRAINT fk_tecnico_idEquipe FOREIGN KEY(idEquipe)
    REFERENCES Equipe(id)
);

INSERT INTO Tecnico (id, cpf, nome, idEquipe, dataNasc) 
  VALUES (1, '123.654.875-90', 'Marcelo de Oliveira', 1, '1965-03-04');
INSERT INTO Tecnico (id, cpf, nome, idEquipe, dataNasc) 
  VALUES (2, '565.187.765-12', 'Dorival Junior', 2, '1962-04-25');
INSERT INTO Tecnico (id, cpf, nome, idEquipe, dataNasc) 
  VALUES (3, '098.904.642-65', 'Tite', 3, '1961-05-25');
INSERT INTO Tecnico (id, cpf, nome, idEquipe, dataNasc) 
  VALUES (4, '187.644.235-20', 'Osorio', 4, '1962-06-08');

CREATE TABLE PaisesTecnicos (
  idTecnico INT,
  pais VARCHAR(32),
  PRIMARY KEY (idTecnico, pais),
  FOREIGN KEY (idTecnico)
    REFERENCES Tecnico(id)
    ON DELETE CASCADE
);

INSERT INTO PaisesTecnicos (idTecnico, pais) VALUES (1, 'Brasil');
INSERT INTO PaisesTecnicos (idTecnico, pais) VALUES (2, 'Brasil');
INSERT INTO PaisesTecnicos (idTecnico, pais) VALUES (3, 'Brasil');
INSERT INTO PaisesTecnicos (idTecnico, pais) VALUES (3, 'Emirados Arabes');
INSERT INTO PaisesTecnicos (idTecnico, pais) VALUES (4, 'Estados Unidos');
INSERT INTO PaisesTecnicos (idTecnico, pais) VALUES (4, 'Colombia');
INSERT INTO PaisesTecnicos (idTecnico, pais) VALUES (4, 'Mexico');
INSERT INTO PaisesTecnicos (idTecnico, pais) VALUES (4, 'Brasil');

CREATE TABLE Jogo (
  id INT AUTO_INCREMENT PRIMARY KEY,
  dataJogo DATE,
  idEquipeCasa INT,
  idEquipeFora INT,
  golsEquipeCasa INT,
  golsEquipeFora INT,
  idCidade INT,
  estadio VARCHAR(32),
  idCampeonato INT,
  FOREIGN KEY (idEquipeCasa)
    REFERENCES Equipe (id),
  FOREIGN KEY (idEquipeFora)
    REFERENCES Equipe (id),
  FOREIGN KEY (idCidade)
    REFERENCES Cidade (id)
    ON DELETE SET NULL,
  FOREIGN KEY (idCampeonato)
    REFERENCES Campeonato (id)
);

INSERT INTO Jogo (id, dataJogo, idEquipeCasa, idEquipeFora, 
                golsEquipeCasa, golsEquipeFora, idCidade, estadio, idCampeonato)
  VALUES (1, '2015-06-10', 3, 1, 0, 2, 1, 'Itaquerao', 1);
INSERT INTO Jogo (id, dataJogo, idEquipeCasa, idEquipeFora, 
                golsEquipeCasa, golsEquipeFora, idCidade, estadio, idCampeonato)
  VALUES (2, '2015-06-11', 2, 4, 2, 2, 1, 'Vila Belmiro', 1);
INSERT INTO Jogo (id, dataJogo, idEquipeCasa, idEquipeFora, 
                golsEquipeCasa, golsEquipeFora, idCidade, estadio, idCampeonato)
  VALUES (3, '2015-06-11', 2, 3, 3, 2, NULL, 'Morumbi', 1);


INSERT INTO equipe (nome) VALUES ('Flamengo');
INSERT INTO equipe (nome) VALUES ('Fluminense');
INSERT INTO equipe (nome) VALUES ('Vasco');
INSERT INTO equipe (nome) VALUES ('Gremio');
INSERT INTO equipe (nome) VALUES ('Internacional');
INSERT INTO equipe (nome) VALUES ('Atletico PR');
INSERT INTO equipe (nome) VALUES ('Coritiba');
INSERT INTO equipe (nome) VALUES ('Atletico MG');
INSERT INTO equipe (nome) VALUES ('Cruzeiro');
INSERT INTO equipe (nome) VALUES ('Bahia');
INSERT INTO equipe (nome) VALUES ('Vitoria');
INSERT INTO equipe (nome) VALUES ('Sport');
INSERT INTO equipe (nome) VALUES ('Nautico');
INSERT INTO equipe (nome) VALUES ('Ponte Preta');
INSERT INTO equipe (nome) VALUES ('Guarani');
INSERT INTO equipe (nome) VALUES ('Portuguesa');

select * from equipe;

# ***********************
# ********* INDICES *****
# ***********************

create table TORCEDOR(
 id int,
 nome varchar(30),
 sexo char(1),
 idEquipe int,
 constraint pk_torcedor primary key(id),
 constraint fk_torcedor_equipe foreign key(idEquipe)
 references Equipe(id)
 );

create table TORCEDOR2(
 id int,
 nome varchar(30),
 sexo char(1),
 idEquipe int,
 constraint pk_torcedor2 primary key(id),
 constraint fk_torcedor_equipe2 foreign key(idEquipe)
 references Equipe(id)
 );

EXPLAIN select * from torcedor where id = 5;

DELIMITER $$

CREATE PROCEDURE popular_torcedores()
BEGIN
    DECLARE i INT DEFAULT 1;
    WHILE i <= 100000 DO
        INSERT INTO torcedor(id, nome)
        VALUES(i, CONCAT('torcedor', LPAD(i, 6, '0')));
        INSERT INTO torcedor2(id, nome)
        VALUES(i, CONCAT('torcedor2', LPAD(i, 6, '0')));
        IF MOD(i, 10000) = 0 THEN
            COMMIT;
        END IF;
        SET i = i + 1;
    END WHILE;
    COMMIT;
END $$

DELIMITER ;

SELECT * FROM torcedor;
-- contar o tempo de execução
-- Ativar profiling
SET PROFILING = 1;

-- Consulta de exemplo
SELECT * FROM torcedor WHERE nome = 'Torcedor000123';

-- Execute a procedure SEPARADAMENTE para evitar erro de "out of sync"
CALL popular_torcedores();

-- Depois, consulte os tempos
SHOW PROFILES;

-- Atualizar sexos
UPDATE Torcedor SET sexo = 'M' WHERE MOD(id, 2) = 0;
UPDATE Torcedor SET sexo = 'F' WHERE MOD(id, 2) = 1;
UPDATE Torcedor2 SET sexo = 'M' WHERE MOD(id, 2) = 0;
UPDATE Torcedor2 SET sexo = 'F' WHERE MOD(id, 2) = 1;

-- Corrigir a variável 'i' -> usar 'id'
UPDATE Torcedor SET idEquipe = MOD(id, 10) + 1;
UPDATE Torcedor2 SET idEquipe = MOD(id, 10) + 1;

-- Somente depois, se quiser, remova a procedure
DROP PROCEDURE IF EXISTS popular_torcedores;

ALTER TABLE JogadorBrasileiro
ADD COLUMN DataUltimaAlteracao datetime,
ADD COLUMN UsuarioUltimaAlteracao varchar(16),
ADD COLUMN operacao varchar(16);

DELIMITER //

CREATE TRIGGER TR_RegistraAlteracaoJogadorBR
BEFORE INSERT ON JogadorBrasileiro
FOR EACH ROW
BEGIN
	SET NEW.DataUltimaAlteracao = NOW();
    	SET NEW.UsuarioUltimaAlteracao = CURRENT_USER();
    	SET NEW.operacao = 'INSERT';
END;
// 
CREATE TRIGGER Tr_RegistraAlteracaoJogadorBR_UPDATE
BEFORE UPDATE ON JogadorBrasileiro
FOR EACH ROW
BEGIN
	SET NEW.DataUltimaAlteracao = NOW();
	SET NEW.UsuarioUltimaAlteracao = current_user();
	SET NEW.operacao = 'UPDATE';
END;
//
DELIMITER ;

UPDATE JogadorBrasileiro
SET salario = salario * 1.1
where nome like 'Sao Marcos';

insert INTO JogadorBrasileiro (cpf, nome, posicao, idEquipe, salario)
values ('064.174.178.09', 'Juca Bala', 'Goleiro', 7, 10900);

CREATE TABLE auditoriaJogadorBr (
	idJogadorBr INT,
    salarioAntigo DECIMAL(10,2),
    salNovo decimal(10,2),
    usuario varchar(16),
    dataAlteracao datetime
);

DELIMITER //
CREATE TRIGGER tr_auditoriaSalarioJogadorBr
BEFORE UPDATE ON JogadorBrasileiro
FOR EACH ROW
BEGIN
 IF OLD.salario <> NEW.salario THEN
	INSERT INTO auditoriaJogadorBr (idJogadorBr, salarioAntigo, salNovo, usuario, dataAlteracao)
    values (OLD.id, OLD.salario, NEW.salario, CURRENT_USER(), NOW());
END IF;
END;
//
DELIMITER ;

Select * from JogadorBrasileiro;

UPDATE JogadorBrasileiro set salario = salario*1.1
	WHERE nome LIKE 'Sao Marcos';

DROP TRIGGER tr_auditoriaSalarioJogadorBr;
-- Exemplo com varialvel de controle 
SET @habilitar_auditoria = 1;
DELIMITER //
CREATE TRIGGER tr_auditoriaSalarioJogadorBr
BEFORE UPDATE ON JogadorBrasileiro
FOR EACH ROW
BEGIN
	IF @habilitar_auditoria = 1 AND OLD.salario <> NEW.salario THEN
    insert INTO auditoriaJogadorBr (idJogadorBr, salarioAntigo, salNovo, usuario, dataAlteracao)
    values (OLD.id, OLD.salario, NEW.salario, CURRENT_USER(), NOW());
    END IF;
END;
// 
DELIMITER ;

# ***********************
# ******* ATIVIDADE *****
# ***********************




CREATE TABLE registroCartao (
id INT PRIMARY KEY AUTO_INCREMENT,
id_jogador INT,
origem ENUM('brasileiro', 'estrangeiro') NOT NULL,
tipo ENUM('amarelo', 'vermelho') NOT NULL,
data_aplicacao DATETIME DEFAULT CURRENT_TIMESTAMP
);

Alter table jogadorBrasileiro
add column cartoes int default 0;

Alter table jogadorEstrangeiro
add column cartoes int default 0;

# criando trigger

DELIMITER $$

CREATE TRIGGER atualiza_cartoes
AFTER INSERT ON registroCartao
FOR EACH ROW
BEGIN
 IF NEW.origem = 'brasileiro' THEN
	UPDATE JogadorBrasileiro
    SET cartoes = cartoes + 1
    WHERE id = NEW.id_jogador;
 ELSEIF NEW.origem = 'estrangeiro' THEN
	UPDATE JogadorEstrangeiro
    SET cartoes = cartoes + 1
    WHERE id = NEW.id_jogador;
 END IF;
END $$
DELIMITER ;

select * from registroCartao;
select * from JogadorBrasileiro;

INSERT INTO registroCartao(id_jogador, origem, tipo)
VALUES(1, 'brasileiro', 'amarelo');

INSERT INTO registroCartao(id_jogador, origem, tipo)
VALUES(1, 'brasileiro', 'amarelo');

INSERT INTO registroCartao(id_jogador, origem, tipo)
VALUES(1, 'brasileiro', 'amarelo');

show warnings;

select id, nome, cartao from jogadorBrasileiro where id = 1;

CREATE TABLE log_mensagens (
id INT AUTO_INCREMENT PRIMARY KEY,
id_jogador INT,
mensagem TEXT,
data_evento DATETIME DEFAULT CURRENT_TIMESTAMP
);


# --------------------------- #
# -------- ATIVIDADE -------- #
# --------------------------- #

CREATE TABLE log_mensagens (
id INT AUTO_INCREMENT PRIMARY KEY,
id_jogador INT,
mensagem TEXT,
data_evento DATETIME DEFAULT CURRENT_TIMESTAMP
);

DROP TRIGGER verifica_cartoes;

DELIMITER $$

CREATE TRIGGER verifica_cartoes
BEFORE INSERT ON registroCartao
FOR EACH ROW
BEGIN
  DECLARE qtd_amarelos INT;

  IF NEW.tipo = 'amarelo' THEN
    SELECT COUNT(*) INTO qtd_amarelos
    FROM registroCartao
    WHERE id_jogador = NEW.id_jogador AND tipo = 'amarelo';

    IF qtd_amarelos = 2 THEN
      SET NEW.tipo = 'vermelho';

      INSERT INTO log_mensagens(id_jogador, mensagem)
      VALUES (NEW.id_jogador, 'Jogador recebeu terceiro cartão amarelo, convertido para vermelho');

      INSERT INTO log_mensagens(id_jogador, mensagem)
      VALUES (NEW.id_jogador, 'Jogador expulso por acúmulo de cartões amarelos');
    END IF;
  END IF;
END$$

DELIMITER ;
 
