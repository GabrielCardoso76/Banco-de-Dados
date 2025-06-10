DROP DATABASE IF EXISTS P2_BD_Gabriel_Cardoso;
CREATE DATABASE IF NOT EXISTS P2_BD_Gabriel_Cardoso;
USE P2_BD_Gabriel_Cardoso;
-- show databases;
-- describe ou desc funcionario;
-- show tables

-- Inicio da Execucao com usuario futebol
-- Remover tabelas do banco (ordem importa)
/*
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


ALTER TABLE Jogo ADD CONSTRAINT fk_jogo_cidade 
  FOREIGN KEY(idCidade) REFERENCES Cidade(id) ON DELETE SET NULL;


select * from equipe;


#**************************************
#************* QUESTÕES ***************
#**************************************


#1) Crie uma view chamada vw_equipes_campeonato que mostre o nome de todas as equipes que participam de algum campeonato e a posição delas.
create view vw_equipes_campeonato AS select e.nome, ec.posicao
from equipe e
join EquipeCampeonato ec ON e.id = ec.idEquipe;

select * from vw_equipes_campeonato;

#2) Crie uma view chamada vw_tecnicos_brasileiros que liste apenas o nome dos técnicos brasileiros (considerando que Brasil está na tabela PaisesTecnicos).

create view vw_tecnicos_brasileiros as select t.nome
from tecnico t 
join PaisesTecnicos pt on t.id = pt.idTecnico
where pt.pais = "Brasil";

select * from vw_tecnicos_brasileiros;

#3) Crie uma view chamada vw_jogadores_sem_equipe que mostre o nome e a posição de todos os jogadores (brasileiros e estrangeiros) que atualmente não estão associados a nenhuma equipe, ou seja, o id da equipe é NULL.

create view vw_jogadores_sem_equipe as select nome, posicao
from JogadorBrasileiro where idEquipe is null 
union all 
select nome, posicao from JogadorEstrangeiro
where IdEquipe is null;

select * from vw_jogadores_sem_equipe;

#**************************************
#************** INDEX *****************
#**************************************
#Indexes são como o índice de um livro: eles ajudam o banco de dados a encontrar informações muito mais rápido.
#1) Crie um índice na coluna nome da tabela JogadorBrasileiro para agilizar buscas por nome de jogador.

create INDEX idx_JogadorBrasileiro_nome ON
jogadorBrasileiro(nome);

#2)Crie um índice na coluna dataJogo da tabela Jogo para otimizar consultas baseadas na data dos jogos.

create index idx_jogo_dataJogo ON 
jogo(dataJogo);

#3) Crie um índice na coluna salario da tabela JogadorBrasileiro para otimizar consultas que filtram ou ordenam por salário.

create index idx_jogadorbrasileiro ON 
jogadorbrasileiro(salario);

#**************** TRIGGERS *******************
#Triggers são ações automáticas que acontecem no banco de dados quando algo específico (como inserir ou atualizar dados) ocorre.
#1) Crie um TRIGGER before_insert_jogadorbrasileiro_posicao que, antes de inserir um novo jogador brasileiro, padronize a posição para "Meio-Campo" se ela for nula.

DELIMITER $$

create trigger before_insert_jogadorbrasileiro_posicao
before insert ON jogadorBrasileiro for each row
begin 
	if new.posicao is null
    then set new.posicao = 'Meio-Campo';
    end if;
end$$
DELIMITER ;

#2)Crie um TRIGGER after_insert_nova_equipe_log que, após a inserção de uma nova equipe na tabela Equipe, registre o nome da nova equipe e a data de inserção em uma tabela de log simples (crie a tabela log_equipes_novas primeiro). Considere a tabela log_equipes_novas.

CREATE TABLE log_equipes_novas (
    id_log INT AUTO_INCREMENT PRIMARY KEY,
    nomeEquipe VARCHAR(32),
    dataInsercao DATETIME DEFAULT CURRENT_TIMESTAMP
);

DELIMITER $$

create trigger after_insert_nova_equipe_log
after insert On equipe for each row
begin
insert into log_equipes_novas(nomeEquipe) Values (NEW.nome);
end$$

DELIMITER ;

show triggers;

# 3) Crie um TRIGGER before_insert_jogo_gols_nao_negativos que, antes de inserir um novo jogo, garanta que os golsEquipeCasa e golsEquipeFora
-- não sejam negativos. Se algum for, defina-o como 0.
DELIMITER $$

create trigger before_insert_jogo_gols_nao_negativos
before insert ON jogo for each row
begin
	if NEW.golsEquipeCasa < 0 then
	set NEW.golsEquipeCasa = 0;
	end if;
	if NEW.golsEquipeFora < 0 then
	set NEW.golsEquipeFora = 0;
	end if;
end$$

DELIMITER ;

show triggers;

#**************** EVENTS *******************
#Events são tarefas que o banco de dados executa automaticamente em horários definidos, como um despertador.
#1) Crie um EVENTO atualizar_salarios_zero_mensal que, no primeiro dia de cada mês, defina o salário de todos os jogadores brasileiros e estrangeiros para 0.

-- set o scheduler aqui !!!
set global event_scheduler = ON;

DELIMITER $$
CREATE EVENT atualizar_salarios_zero_mensal
ON SCHEDULE EVERY 1 MONTH
STARTS '2025-07-01 00:00:00' -- Definido para o próximo primeiro dia do mês
DO
BEGIN
   update JogadorBrasileiro SET salario = 0;
   update JogadorEstrangeiro SET salario = 0;
END$$
DELIMITER ;


#2) Crie um EVENTO limpar_jogos_antigos_semanal que, toda segunda-feira, exclua da tabela Jogo todos os jogos com data anterior a 1 ano atrás
pesquise sobre a funcao DATE_SUB.
DELIMITER $$
CREATE EVENT limpar_jogos_antigos_semanal
ON SCHEDULE every 1 week
STARTS '2025-06-16 00:00:00'    -- Defina para a próxima segunda-feira (use o exemplo da questao 1 para setar data e hora)
DO
BEGIN
    delete from Jogo where dataJogo < date_sub(now(), interval 1 year);
END$$
DELIMITER ;


#3) Crie um EVENTO atualizar_salarios_minimos_semanal que, toda segunda-feira, verifique todos os jogadores brasileiros e, se o salário deles 
-- for menor que R$ 10.000,00, ajuste-o para R$ 10.000,00. Isso simula um "salário mínimo" garantido pelo clube.
-- Certifique-se de que o agendador de eventos esteja ligado

DELIMITER $$
CREATE EVENT atualizar_salarios_minimos_semanal
ON SCHEDULE every 1 week
STARTS '2025-06-16 00:00:00'    
DO
BEGIN
    update JogadorBrasileiro set salario = 10000.00 
    where salario < 10000.00;
END$$
DELIMITER ;

show events;

# ****************************************
#**********STORED PROCEDURES *************
# ****************************************
#Stored procedures são blocos de código que você salva no banco de dados e pode chamar a qualquer momento, como um atalho para tarefas comuns.
#1)Crie uma Stored Procedure sp_listar_todas_equipes que simplesmente liste todas as equipes existentes na tabela Equipe.

DELIMITER $$
create procedure sp_listar_todas_equipes()
begin
	select * from equipe;
    END$$
DELIMITER ;
#2) Crie uma Stored Procedure sp_contar_jogadores_por_posicao que receba uma posição (ex: 'Atacante', 'Goleiro') como parâmetro e retorne o número de jogadores brasileiros nessa posição.
DELIMITER $$
CREATE PROCEDURE sp_contar_jogadores_por_posicao(in p_posicao varchar(16), OUT p_total int)
BEGIN
    select count(*) into p_total from JogadoresBrasileiro 
    where posicao = p_posicao;
END$$
DELIMITER ;

#3) Crie uma Stored Procedure sp_adicionar_novo_campeonato que receba o nome de um campeonato como parâmetro e o adicione à tabela Campeonato.

DELIMITER $$
create procedure sp_adicionar_novo_campeonato(in p_nome VARCHAR(32))
begin
 insert into Campeonato (nome)
 values (p_nome);
 end$$
DELIMITER ;

show procedure status;

#***************** FUNCTION ******************

#Funções no MySQL sempre retornam um único valor, e podemos adicionar lógica condicional com IF ELSE para que elas tomem decisões.

#1)Crie uma FUNCTION fn_status_salario_jogador que receba o id de um jogador brasileiro como parâmetro. A função deve verificar o salário do jogador e retornar uma string:
/*
'Salário Alto' se o salário for maior que R$ 300.000,00.
'Salário Médio' se o salário estiver entre R$ 50.000,00 e R$ 300.000,00 (inclusive).
'Salário Baixo' se o salário for menor que R$ 50.000,00.
*/

DELIMITER $$
CREATE FUNCTION fn_status_salario_jogador(p_id_jogador INT)
RETURNS VARCHAR(30)
deterministic
BEGIN
	declare v_salario int;
    select salario into v_salario
    from JOgadorBrasileiro where id = p_id_jogador;
    if v_salario > 300000 then 
    return 'Salario Alto';
    elseif v_salario >= 50000 then
    return 'Salario Medio';
    else
    return 'Salario Baixo';
    end if;

END$$
DELIMITER ;


#2) Crie uma FUNCTION fn_total_gols_jogo que receba o id de um jogo e retorne a soma dos gols das duas equipes naquele jogo.

DELIMITER $$ 
create function fn_total_gols_jogo(p_id_jogo INT)
returns int
deterministic
begin
	declare v_total_gols int;
    select golsEquipeCasa + golsEquipeFora 
    into v_total_gols from jogo 
    where id = p_id_jogo;
    return v_total_gols;
    end$$
DELIMITER ;



#3)Crie uma FUNCTION fn_contar_equipes que retorne o número total de equipes cadastradas.

DELIMITER $$ 
	create function fn_contar_equipes()
	returns int 
	deterministic
	begin
	declare v_total_equipes int;
	select count(*) into v_total_equipes
	from Equipe;
	return v_total_equipes;
	END$$
DELIMITER ;

show function status;

# ************** QUESTÃO EXTRA [1,0 pto] ****************
/* Depois que você terminou sua avaliação, faça para esse mesmo script fornecido:
Crie um novo usuário em seu ambiente MySQL, dando a ele um nome de usuário e uma senha de sua escolha. 

a) Conceda permissões totais a este novo usuário em todos os bancos de dados e tabelas.
b) Verifique as permissões concedidas ao usuario_teste para confirmar que ele possui acesso total. (Dica: pesquise como listar as permissões de um usuário específico).
c) Retire todas as permissões concedidas a este usuário.
d) Verifique novamente as permissões do usuario_teste para confirmar que elas foram revogadas.
*/
# OBS: Todas as questoes tem o mesmo peso, exceto a questão EXTRA. A prova vale 10,0 pontos + 1,0 ponto EXTRA!

create user 'Cardoso'@'localhost' 
IDENTIFIED BY 'senai123';

#a)
grant all privileges on *.* to
'Cardoso'@'localhost';

#b)
show grants for 'Cardoso'@'localhost';

#c)
REVOKE All privileges on *.* 
from 'Cardoso'@'localhost'
privileges;

#d)
show grants for 'Cardoso'@'localhost';