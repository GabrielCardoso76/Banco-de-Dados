DROP DATABASE IF EXISTS AVP2_GABRIEL_CARDOSO;

CREATE DATABASE IF NOT EXISTS AVP2_GABRIEL_CARDOSO;

USE AVP2_GABRIEL_CARDOSO;

#DROP TABLE IF EXISTS CAMINHAO;

#criar a tabela caminhao
CREATE TABLE IF NOT EXISTS CAMINHAO(
codigoC integer not null,
capacidade float,
marca varchar(20),
modelo varchar(20),
primary key(codigoC)
);
#DROP TABLE IF EXISTS PRODUTO;

#criar a tabela produto
CREATE TABLE IF NOT EXISTS PRODUTO(
codigoP integer not null,
marca varchar(20),
nome varchar(20),
fabricante varchar(32),
primary key(codigoP)
);
DROP TABLE IF EXISTS MOTORISTA;

#criar a tabela motorista
CREATE TABLE IF NOT EXISTS MOTORISTA(
cpf varchar(32) not null,
nome varchar(32) not null,
idade integer,
endereco varchar(32),
primary key (cpf)
);

#DROP TABLE IF EXISTS VIAGEM;

#criar a tabela viagem
CREATE TABLE IF NOT EXISTS VIAGEM(
dataInicio date not null,
dataFim date,
cpf varchar (32),
codigoC integer not null,
primary key (dataInicio,cpf,codigoC),
foreign key (codigoC) references caminhao (codigoC),
foreign key (cpf) references MOTORISTA (cpf)
);
# tabela transporta criada
#DROP TABLE IF EXISTS TRANSPORTA;

CREATE TABLE IF NOT EXISTS TRANSPORTA (
    DATA_INICIO DATE NOT NULL,
    CPF VARCHAR(15) NOT NULL,
    CODIGOC INT NOT NULL,
    CODIGOP INT NOT NULL,
    PRIMARY KEY (DATA_INICIO , CPF , CODIGOC , CODIGOP),
    FOREIGN KEY (DATA_INICIO , CPF , CODIGOC)
        REFERENCES VIAGEM (DATAINICIO , CPF , CODIGOC)
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (CODIGOP)
        REFERENCES PRODUTO (CODIGOP)
        ON UPDATE CASCADE ON DELETE CASCADE
);

# ** INSERTS **

INSERT INTO CAMINHAO VALUES (1,null, 'MERCEDEZ', 'BW12');
INSERT INTO CAMINHAO VALUES (2,null, 'SCANIA', 'AD23');
INSERT INTO CAMINHAO VALUES (3,null, 'MERCEDEZ', 'TRUCK');
INSERT INTO CAMINHAO VALUES (4,null, 'FORD', 'ERON');
INSERT INTO CAMINHAO VALUES (5,null, 'SCANIA', 'THOR');

INSERT INTO PRODUTO VALUES (1, 'SOIL', 'SOJA', 'SOJALU');
INSERT INTO PRODUTO VALUES (2, 'GARLIC', 'ALHO', 'SOJALU');
INSERT INTO PRODUTO VALUES (3, 'ONION', 'CEBOLA', 'CREMESP');
INSERT INTO PRODUTO VALUES (4, 'SALT', 'SAL', 'CREMESP');
INSERT INTO PRODUTO VALUES (5, 'OIL', 'AZEITE', 'GALO');

INSERT INTO MOTORISTA VALUES ('123', 'CAROL', 32, 'RUA SAO BENTO, 22');
INSERT INTO MOTORISTA VALUES ('234', 'ANTONIO', 40, 'RUA JOAQUIM BARBOSA, 21');
INSERT INTO MOTORISTA VALUES ('456', 'JOANA', 28, 'RUA AMARANTHUS, 43');
INSERT INTO MOTORISTA VALUES ('347', 'LUIZ', 21, 'RUA GHOST, 54');
INSERT INTO MOTORISTA VALUES ('555', 'TEREZA', 55, 'RUA THEODORO, 66');

INSERT INTO VIAGEM VALUES ('2019-04-12', '2019-05-15', '123', 1);
INSERT INTO VIAGEM VALUES ('2019-05-15', '2019-06-16', '123', 2);
INSERT INTO VIAGEM VALUES ('2019-05-31', NULL, '234', 2);
INSERT INTO VIAGEM VALUES ('2019-07-08', NULL, '456', 3);
INSERT INTO VIAGEM VALUES ('2019-08-15', NULL, '347', 3);

INSERT INTO TRANSPORTA VALUES ('2019-04-12', '123', 1, 1);
INSERT INTO TRANSPORTA VALUES ('2019-05-15', '123', 2, 2);
INSERT INTO TRANSPORTA VALUES ('2019-05-31', '234', 2, 3);
INSERT INTO TRANSPORTA VALUES ('2019-07-08', '456', 3, 4);
INSERT INTO TRANSPORTA VALUES ('2019-08-15', '347', 3, 5);

# Responda as questões **SELECTS**:

#(A) mostre a quantidade de caminhões por marca
select count(distinct(marca)) as qtd_marca from caminhao;
#(B) mostre todas as marcas de caminhão que possuem a letra c no nome
select distinct marca from caminhao 
where marca like ('%C%');
#(C) mostre quantos produtos estão cadastrados
select count(codigoP) from produto;
#(D) quantos produtos são do fabricante SOJALU
select count(codigoP) from produto
where fabricante like '%SOJALU%';
#(E) mostre todas as viagens que não foram finalizadas data fim e null
select * from viagem
where dataFim is null;
#(F) mostre todas viagens que já foram finalizadas data fim não e null
select * from viagem 
where datafim is not null;
#(G) mostre os dados dos motoristas nas viagens
select m.* from motorista m, viagem v
where m.cpf = v.cpf;
#(H) mostre os dados do caminhão na viagem
select c.* from caminhao c, viagem v
where c.codigoC = v.codigoC;
#(I) mostre os dados do motorista e os dados do caminhão na viagem
select m.*, c.* from motorista m, caminhao c, viagem v
where m.cpf = v.cpf and c.codigoc = v.codigoc;
#(J) mostre os dados da viagem com os produtos transportados
select v.* from viagem v, transporta t
where v.dataInicio = t.data_inicio;
#(K) mostre os dados da viagem com os dados motorista, os dados do caminhão e os dados dos produtos
select v.* from viagem v, motorista m, caminhao c, produto p;
#(L) selecione as viagens não finalizadas do motorista Antônio
select v.* from viagem v, motorista m 
where m.nome like 'Antonio' and m.cpf = v.cpf and v.dataFim is null;
#(M) selecione as viagens finalizadas da motorista Carol	
select v.* from viagem v, motorista m 
where m.nome like 'Carol' and m.cpf = v.cpf and v.dataFim is not null;
#(N) selecione todas as viagens com caminhões da marca Mercedes
select v.* from viagem v, caminhao c
where V.CODIGOC = C.codigoc and c.marca = '%MERCEDEZ%';
#(O) selecione todas as viagens que transportaram cebola ou alho
select v.* from viagem v, produto p, transporta t
 where t.codigop = p.codigop and t.codigoc = v.codigoc;
#(P) Mostre o nome dos motoristas e, se houver, a data de início das viagens realizadas por eles.
-- (mostra todos os motoristas, mesmo os que nunca fizeram viagem)
SELECT m.nome, v.datainicio from motorista m left join viagem v on m.cpf = v.cpf;
#(Q) Mostre a marca e modelo dos caminhões que já foram usados em alguma viagem.
-- (mostra apenas caminhões que estão em viagens)
select c.marca, c.modelo from caminhao c inner join viagem v on c.codigoc = v.codigoc;
