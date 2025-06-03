#*******EVENTOS*********

/*
agendar tarefas automaticas no BD, backups, limpeza, atualizacoes... 
*/
create database eventos;
use eventos;
#ativando o evento (agendador de tarefas)
SET GLOBAL event_scheduler = ON;

#verificando status 
SHOW variables like 'event_scheduler';
#criar tabela
create table logs(
	id INT auto_increment primary key,
    mensagem varchar(255),
    data_hora datetime
);
create table produtos(
	id INT auto_increment primary key,
    nome varchar(100),
    preco decimal(10,2),
    categoria varchar(50)
);
create table notificacoes(
	id INT auto_increment primary key,
    mensagem varchar(255),
    data_hora datetime
);
#crriando eventos inserir log
create event insere_log
on schedule every 1 minute
do
	insert into log(mensagem, data_hora)
    values ("execução automatica", now());
    
select * from logs;

insert into produtos(nome, preco, categoria)
values ("notebook", 5000.99, "Eletrônicos");

insert into produtos(nome, preco, categoria)
values ("pc", 9000.99, "Eletrônicos");

insert into produtos(nome, preco, categoria)
values ("mouse", 1000.99, "Eletrônicos");

# criando eventos desconto nos produtos
create event aplica_desconto
on schedule at current_timestamp() + interval 1 day
do
	update produtos
	SET preco = preco * 0.9
    where categoria = 'Eletrônicos';
    
select * from produtos;
show events; 
	#evento para limpar logs
create event limpa_logs
on schedule every 1 day
do 
	delete from logs
    where data_hora < NOW() - interval 30 day;
    
#ver o codigo do evento
show create event insere_log;
#remover evento
drop event insere_log;
select * from logs;
#limpar as tabelas
truncate table logs;

select id, nome, preco, categoria from produtos;
#verificar quando o desconto vai ocorrer 
select LAST_ EXECUTE, STATUS FROM information_schema.EVENTS
where EVENT_NAME = 'insere_log';


#*********************************
#******* STORED PROCEDURE ********
#*********************************
/*Teoria:
blocos de procedimentos(reutilizacao)
- automatizo tarefas complexa!
- redução de repedicao de codigo
- padronizar operacoes no banco de dados
*/
create database loja;
use loja;
create table clientes(
	id INT auto_increment primary key,
    nome varchar(100),
    email varchar(100),
    ativo boolean default true
);

create table vendas(
	id INT auto_increment primary key,
    cliente_id int,
    valor decimal(10,2),
    data_venda date,
    foreign key(cliente_id) references clientes(id)
);
-- criando procedures
DELIMITER //
create procedure inserir_cliente(
	in nome_cliente varchar(100),
    in email_cliente varchar(100)
)
begin
	insert into clientes(nome, email) values(nome_cliente, email_cliente);
end // 
DELIMITER ; 

call inserir_cliente('Carlos Alberto','carlos@gmail.com');
select * from clientes;

#calcular total de vendas por cliente
DELIMITER // 
create procedure total_vendas_cliente(
	in cliente int,
    out total decimal(10,2)
)
begin 
	select sum(valor) into total
    from vendas
    where cliente_id = cliente;
end //
DELIMITER ;

# chamar a procedure com variavel de saida
SET @total_vendas = 0;
CALL total_vendas_cliente(1, @total_vendas);
SELECT @total_vendas;
#gerenciar procedure
show procedure status inserir_cliente;
#drop
drop procedure inserir_cliente;

# fazendo teste ******
select * from clientes;
call inserir_cliente('Cliente sem vendas', 'semvendas@teste.com');
#pegar id do cliente inserido no meu banco
set @cliente_id = last_insert_id();
#calcular total de vendas
set @total = 0;
call total_vendas_cliente(@cliente_id, @total);
select @total;

call inserir_cliente('Cliente com vendas', 'comvendas@teste.com');
#pegar o id do cliente inserido no meu banco
SET @cliente_id = last_insert_id();
#inserir vendas para o cliente
insert into vendas(cliente_id, valor, data_venda) values
(@cliente_id, 100.50, '2025-01-01'),
(@cliente_id, 55.70, '2025-01-02'),
(@cliente_id, 55.25, '2025-01-03');
select * from vendas;
#calcular total de vendas
SET @total = 0;
call total_vendas_cliente(@cliente_id, @total);
select @total;

# inserir 100 clientes
DELIMITER //
create procedure inserir_clientes_automatico()
begin 
	declare i int default 1;
    while i <= 100 do 
		call inserir_cliente(CONCAT('Cliente', i), CONCAT('cliente',i, '@teste.com'));
        set i = i + 1;
	end while;
end //

DELIMITER ;

select * from clientes;

call inserir_clientes_automatico();

#************************************
#*************FUNCTION***************
#************************************
/*TEORIA:
blocos de codigo armazenado no BD que executa um calculo e retorna o valor corresponde select, where, order by ent...
- calcular repetitivos
- organizacao de codigo
*/
create database funcao;
use funcao;

DELIMITER //
create function multiplica_por_dois(valor int)
returns int 
deterministic
begin 
	return valor * 2;
end //
DELIMITER ;

select multiplica_por_dois(5);

#criar tabela produtos
create table produtos(
	id int auto_increment primary key,
    nome varchar(100),
    preco decimal(10,2),
    quatidade int
);

insert into produtos (nome, preco, quantidade) values
("notebook dell", 4200.00, 4),
("fone de ouvido", 199.90, 12),
("monitor 24 polegadas", 899.00, 0);

select * from produtos;
# funcao para calcular o valor total de mercadoria!!
DELIMITER //
create function calcular_valor_total(produto_id int)
returns decimal (10,2)
deterministic 
begin 
	declare total decimal(10,2);
    select preco * quantidade into total 
    from produtos
    where id = produto_id;
    return total;
end //
DELIMITER ;
#mostrar o valor total em estoque 
select id, nome, calcular_valor_total(id) as total_em_estoque
from produto;

#mostrar as functions criadas
show function status where Bd = database()s;
    