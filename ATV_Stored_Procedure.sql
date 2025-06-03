
create database empresa;
use empresa;


-- 1. Criação da tabela 'estoque'
CREATE TABLE estoque (
    id INT PRIMARY KEY AUTO_INCREMENT,
    produto VARCHAR(255) NOT NULL UNIQUE, -- UNIQUE para garantir que não haja produtos duplicados
    quantidade INT NOT NULL
);

-- 2. Inserir 3 produtos com diferentes quantidades
INSERT INTO estoque (produto, quantidade) VALUES
('Notebook Dell', 10),
('Mouse Logitech', 50),
('Monitor Samsung', 15);

-- 3. Criar uma procedure chamada registrar_saida
DELIMITER //
CREATE PROCEDURE registrar_saida(
    IN p_nome_produto VARCHAR(255),
    IN p_quantidade_retirar INT
)
BEGIN
    DECLARE v_quantidade_atual INT;

    -- Obter a quantidade atual do produto
    SELECT quantidade INTO v_quantidade_atual
    FROM estoque
    WHERE produto = p_nome_produto;

    -- Verificar se o produto existe
    IF v_quantidade_atual IS NULL THEN
        SELECT 'Erro: Produto não encontrado no estoque.' AS MensagemErro;
    ELSEIF v_quantidade_atual >= p_quantidade_retirar THEN
        -- Atualizar o estoque
        UPDATE estoque
        SET quantidade = quantidade - p_quantidade_retirar
        WHERE produto = p_nome_produto;
        SELECT CONCAT('Saída de ', p_quantidade_retirar, ' unidades de ', p_nome_produto, ' registrada com sucesso. Estoque atual: ', (v_quantidade_atual - p_quantidade_retirar)) AS Mensagem;
    ELSE
        -- Mostrar mensagem de erro se não houver estoque suficiente
        SELECT CONCAT('Erro: Estoque insuficiente para ', p_nome_produto, '. Disponível: ', v_quantidade_atual, ', Tentativa de retirar: ', p_quantidade_retirar) AS MensagemErro;
    END IF;
END //
DELIMITER ;

-- Exemplos de uso da procedure registrar_saida:
CALL registrar_saida('Notebook Dell', 2);   -- Saída bem-sucedida
CALL registrar_saida('Mouse Logitech', 60); -- Estoque insuficiente
CALL registrar_saida('Teclado Mecânico', 5); -- Produto não encontrado

-- 4. Criar uma procedure consultar_estoque
DELIMITER //
CREATE PROCEDURE consultar_estoque(
    IN p_nome_produto VARCHAR(255),
    OUT p_quantidade_disponivel INT
)
BEGIN
    SELECT quantidade INTO p_quantidade_disponivel
    FROM estoque
    WHERE produto = p_nome_produto;

    -- Se o produto não for encontrado, p_quantidade_disponivel será NULL.
    -- Podemos adicionar uma mensagem para isso se necessário, mas o requisito é apenas retornar a quantidade.
END //
DELIMITER ;

-- Exemplos de uso da procedure consultar_estoque:
CALL consultar_estoque('Notebook Dell', @qtd);
SELECT @qtd AS QuantidadeDisponivel;

CALL consultar_estoque('Monitor Samsung', @qtd_monitor);
SELECT @qtd_monitor AS QuantidadeMonitor;

CALL consultar_estoque('Teclado USB', @qtd_teclado);
SELECT @qtd_teclado AS QuantidadeTeclado; -- Deve retornar NULL ou 0 dependendo da configuração do ambiente se o produto não existir.

------------------------------------------------------------------------------------------------------------------------
-- PERGUNTAS E RESPOSTAS (Para Stored Procedures)
------------------------------------------------------------------------------------------------------------------------

-- O que é uma Stored Procedure e qual a sua principal vantagem?
-- Uma Stored Procedure (ou Procedimento Armazenado) é um conjunto de comandos SQL pré-compilados e armazenados no
-- servidor de banco de dados. Ela pode ser executada várias vezes por diferentes aplicações ou usuários.
-- A principal vantagem é a otimização de desempenho, pois a procedure é compilada uma vez e o plano de execução é
-- armazenado em cache, evitando a necessidade de recompilação a cada execução. Além disso, melhora a segurança,
-- encapsula a lógica de negócios e reduz o tráfego de rede entre a aplicação e o banco de dados.

-- Qual a diferença entre parâmetros IN, OUT e INOUT em uma Stored Procedure?
-- - IN (Entrada): O parâmetro IN é usado para passar valores para a procedure. O valor do parâmetro não pode ser
--   modificado dentro da procedure e o valor original é mantido após a execução. É o tipo de parâmetro padrão.
-- - OUT (Saída): O parâmetro OUT é usado para retornar um valor da procedure para o chamador. O valor inicial do
--   parâmetro é NULL dentro da procedure, e qualquer modificação feita nele será visível para o chamador após a
--   execução da procedure.
-- - INOUT (Entrada e Saída): O parâmetro INOUT permite que um valor seja passado para a procedure e, posteriormente,
--   modificado dentro da procedure. O valor modificado é então retornado para o chamador.

-- Quando seria mais adequado usar uma Stored Procedure em vez de uma série de comandos SQL avulsos?
-- É mais adequado usar uma Stored Procedure quando:
-- - Há lógica de negócios complexa que precisa ser executada atomicamente (transações).
-- - A mesma lógica precisa ser reutilizada por diferentes partes da aplicação ou por múltiplas aplicações.
-- - É necessário otimizar o desempenho, reduzindo o tráfego de rede e aproveitando a pré-compilação e cache.
-- - Há requisitos de segurança, permitindo conceder permissão para executar a procedure sem dar acesso direto às tabelas subjacentes.
-- - É preciso garantir a consistência dos dados, aplicando regras de validação ou integridade dentro da procedure.