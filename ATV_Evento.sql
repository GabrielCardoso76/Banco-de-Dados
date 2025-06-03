#Atividade Prática (EVENTO)
#Objetivo: Crie eventos automáticos para simular tarefas do dia a dia de um sistema.

create database evento;
use evento;
#Desafio
#1.Crie uma tabela chamada tarefas com os campos:
# id (INT, chave primária)
# descricao (VARCHAR)
# status (VARCHAR)
create table tarefas(
	id INT auto_increment primary key,
    descricao varchar(255),
    status varchar(55)
);
drop table tarefas;
#2.Insira 5 registros com status 'Pendente'.
insert into tarefas(descricao, status) values
('Limpar terreno', 'Pendente');
insert into tarefas(descricao, status) values
('Lavar lousa', 'Pendente');
insert into tarefas(descricao, status) values
('Arrumar estoque', 'Pendente');
#3.Crie um evento que:
#Muda o status de todas as tarefas para 'Em andamento' a cada 5 minutos.
DELIMITER // 
create event mudar_para_em_andamento
ON schedule every 5 minute
do
begin
	update tarefas 
    set status = "Em andamento" 
    where status = 'Pendente';
END //
DELIMITER ;

#4.Crie outro evento que:
#Após 15 minutos, mude o status das tarefas para 'Finalizado'.
DELIMITER //
CREATE EVENT mudar_para_finalizado
ON SCHEDULE AT CURRENT_TIMESTAMP + INTERVAL 15 MINUTE
DO
BEGIN
    UPDATE tarefas 
    SET status = 'Finalizado' 
    WHERE status = 'Em andamento';
END //
DELIMITER ;
#5.Mostre como visualizar e excluir esses eventos.
SELECT * FROM tarefas;
SHOW EVENTS;
SHOW EVENTS LIKE 'mudar%';
#Perguntas 
#•O que aconteceria se o event_scheduler estivesse desativado?
#•Por que eventos são úteis em um sistema real?
#•Qual a diferença entre evento único e evento recorrente?