#### 1. COMMIT
#### O que é? Confirma e salva todas as alterações da transação no banco.
#### Para que serve? Garante que as mudanças sejam permanentes.
#### Exemplo:

START TRANSACTION;
INSERT INTO clientes (nome, saldo) VALUES ('João', 1000);
COMMIT; -- Salva João com saldo 1000


#### 2. ROLLBACK
#### O que é? Desfaz todas as alterações da transação, voltando ao estado inicial.
#### Para que serve? Reverte mudanças em caso de erro ou falha.
#### Exemplo:

START TRANSACTION;
UPDATE clientes SET saldo = 500 WHERE nome = 'João';
ROLLBACK; -- Cancela a atualização, saldo não muda


#### 3. SAVEPOINT
#### O que é? Marca um ponto na transação para reverter parcialmente.
#### Para que serve? Permite desfazer parte da transação sem perder tudo.
#### Exemplo:

START TRANSACTION;
INSERT INTO clientes (nome, saldo) VALUES ('Ana', 2000);
SAVEPOINT p1;
UPDATE clientes SET saldo = 1500 WHERE nome = 'Ana'; 
ROLLBACK TO p1; -- Desfaz o UPDATE, mantém o INSERT
COMMIT; -- Ana fica com saldo 2000