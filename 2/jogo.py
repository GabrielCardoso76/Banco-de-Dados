import pygame
import sys
import random
import math

# Inicializando o Pygame e o mixer
pygame.init()
pygame.mixer.init()

# --- Configurações da Tela (MODO TELA CHEIA) ---
info_tela = pygame.display.Info()
largura_tela = info_tela.current_w
altura_tela = info_tela.current_h
tela = pygame.display.set_mode((largura_tela, altura_tela), pygame.FULLSCREEN)
pygame.display.set_caption("Alexandre, o Rei")

# --- Cores e Constantes ---
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (50, 50, 255)
AMARELO = (255, 255, 0)
CINZA_ESCURO = (40, 40, 40)
LARANJA = (255, 165, 0)
ROXO = (128, 0, 128)
CIANO = (0, 255, 255)
DANO_COLISAO = 40
CORES_NAVE = [AZUL, AMARELO, VERDE, ROXO, CIANO, BRANCO]

# --- Relógio do Jogo ---
relogio = pygame.time.Clock()
FPS = 60

# --- Classe do Jogador (Nave) ---
class Nave(pygame.sprite.Sprite):
    def __init__(self, x, y, cor, controles, numero_jogador):
        super().__init__()
        self.numero_jogador = numero_jogador
        self.controles = controles
        try:
            self.cor_atual_index = CORES_NAVE.index(cor)
        except ValueError:
            self.cor_atual_index = 0
        self.cor = CORES_NAVE[self.cor_atual_index]
        self.imagem_original = pygame.Surface((50, 30), pygame.SRCALPHA)
        self.image = self.imagem_original.copy()
        self.atualizar_imagem()
        self.rect = self.image.get_rect(center=(x, y))
        
        # Atributos de Upgrade
        self.velocidade_base = 7
        self.dano_tiro_base = 15
        self.cadencia_tiro_base = 200
        self.nivel_velocidade = 0
        self.nivel_dano = 0
        self.nivel_cadencia = 0
        self.velocidade = self.velocidade_base
        self.dano_tiro = self.dano_tiro_base
        self.cadencia_tiro = self.cadencia_tiro_base
        self.vida = 100
        self.vida_maxima = 100
        self.dinheiro = 0
        self.ultimo_tiro = pygame.time.get_ticks()
        
        # Sistema de Calor
        self.calor_atual = 0
        self.calor_maximo = 100
        self.taxa_aumento_calor = 8
        self.taxa_resfriamento = 12
        self.superaquecido = False
        self.tempo_superaquecimento = 0
        self.duracao_cooldown = 3000

    def atualizar_imagem(self):
        self.imagem_original.fill((0, 0, 0, 0))
        pygame.draw.polygon(self.imagem_original, self.cor, [(50, 15), (0, 0), (0, 30)])
        self.image = self.imagem_original

    def update(self, dt):
        teclas = pygame.key.get_pressed()
        if teclas[self.controles['esquerda']] and self.rect.left > 0: self.rect.x -= self.velocidade
        if teclas[self.controles['direita']] and self.rect.right < largura_tela: self.rect.x += self.velocidade
        if teclas[self.controles['cima']] and self.rect.top > 0: self.rect.y -= self.velocidade
        if teclas[self.controles['baixo']] and self.rect.bottom < altura_tela: self.rect.y += self.velocidade
        
        if teclas[self.controles['tiro']]:
            self.atirar()
        
        if not self.superaquecido and self.calor_atual > 0:
            self.calor_atual -= self.taxa_resfriamento * dt
            if self.calor_atual < 0: self.calor_atual = 0
        
        if self.superaquecido:
            if pygame.time.get_ticks() - self.tempo_superaquecimento > self.duracao_cooldown:
                self.superaquecido = False
                self.calor_atual = 0

    def atirar(self):
        if self.superaquecido:
            return

        agora = pygame.time.get_ticks()
        if agora - self.ultimo_tiro > self.cadencia_tiro:
            self.ultimo_tiro = agora
            tiro = TiroJogador(self.rect.right, self.rect.centery, self.dano_tiro, self.cor)
            todos_sprites.add(tiro)
            grupo_tiros_jogadores.add(tiro)
            
            self.calor_atual += self.taxa_aumento_calor
            if self.calor_atual >= self.calor_maximo:
                self.calor_atual = self.calor_maximo
                self.superaquecido = True
                self.tempo_superaquecimento = pygame.time.get_ticks()

    def receber_dano(self, dano):
        self.vida -= dano
        if self.vida <= 0:
            self.vida = 0
            self.kill()

    def reset_stats(self):
        self.nivel_velocidade = 0; self.nivel_dano = 0; self.nivel_cadencia = 0
        self.velocidade = self.velocidade_base; self.dano_tiro = self.dano_tiro_base; self.cadencia_tiro = self.cadencia_tiro_base

# --- Classes de Tiros ---
class TiroJogador(pygame.sprite.Sprite):
    def __init__(self, x, y, dano, cor):
        super().__init__()
        self.image = pygame.Surface((15, 4))
        self.image.fill(cor)
        self.rect = self.image.get_rect(midleft=(x, y))
        self.velocidade = 15
        self.dano = dano

    def update(self, dt):
        self.rect.x += self.velocidade
        if self.rect.left > largura_tela:
            self.kill()

class TiroInimigo(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((12, 4))
        self.image.fill(LARANJA)
        self.rect = self.image.get_rect(midright=(x, y))
        self.velocidade_x = -8
        self.dano = 10

    def update(self, dt):
        self.rect.x += self.velocidade_x
        if self.rect.right < 0:
            self.kill()

class TiroBoss(pygame.sprite.Sprite):
    def __init__(self, x, y, angulo):
        super().__init__()
        self.image = pygame.Surface((10, 10), pygame.SRCALPHA)
        pygame.draw.circle(self.image, VERMELHO, (5, 5), 5)
        self.rect = self.image.get_rect(center=(x, y))
        self.velocidade = 6
        self.dano = 15
        radianos = math.radians(angulo)
        self.velocidade_x = math.cos(radianos) * self.velocidade
        self.velocidade_y = math.sin(radianos) * self.velocidade

    def update(self, dt):
        self.rect.x += self.velocidade_x
        self.rect.y += self.velocidade_y
        if not tela.get_rect().colliderect(self.rect):
            self.kill()

# --- Classes de Inimigos ---
class Inimigo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 35), pygame.SRCALPHA)
        pygame.draw.polygon(self.image, VERMELHO, [(0, 17.5), (40, 0), (40, 35)])
        self.rect = self.image.get_rect(center=(largura_tela + 50, random.randint(50, altura_tela - 50)))
        self.velocidade_x = random.randint(2, 5)
        self.vida = 30
        self.ultimo_tiro = pygame.time.get_ticks()
        self.cadencia_tiro = 2500

    def update(self, dt):
        self.rect.x -= self.velocidade_x
        if self.rect.right < 0:
            self.kill()
        self.atirar()

    def atirar(self):
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_tiro > self.cadencia_tiro:
            self.ultimo_tiro = agora
            tiro = TiroInimigo(self.rect.left, self.rect.centery)
            todos_sprites.add(tiro)
            grupo_tiros_inimigos.add(tiro)

class Boss(pygame.sprite.Sprite):
    def __init__(self, nivel, jogadores_vivos):
        super().__init__()
        self.jogadores_vivos = jogadores_vivos
        self.nivel = nivel
        largura_boss = 120 + nivel * 15
        altura_boss = 100 + nivel * 15
        self.image = pygame.Surface((largura_boss, altura_boss), pygame.SRCALPHA)
        pygame.draw.rect(self.image, VERMELHO, (0, 0, largura_boss, altura_boss), border_radius=15)
        self.rect = self.image.get_rect(midright=(largura_tela - 20, altura_tela / 2))
        self.vida = 1000 + nivel * 300
        self.vida_maxima = self.vida
        self.velocidade_y = 2 + nivel * 0.5
        self.velocidade_x = 1 + nivel * 0.2
        self.timers = {'radial': pygame.time.get_ticks(), 'mira': pygame.time.get_ticks()}
        self.cadencias = {'radial': max(1000, 3000 - nivel * 200), 'mira': max(500, 2000 - nivel * 150)}

    def update(self, dt):
        self.rect.y += self.velocidade_y
        self.rect.x -= self.velocidade_x
        if self.rect.top < 0: self.rect.top = 0; self.velocidade_y *= -1
        if self.rect.bottom > altura_tela: self.rect.bottom = altura_tela; self.velocidade_y *= -1
        if self.rect.left < largura_tela * 0.6: self.rect.left = int(largura_tela * 0.6); self.velocidade_x *= -1
        if self.rect.right > largura_tela: self.rect.right = largura_tela; self.velocidade_x *= -1
        self.atirar()

    def atirar(self):
        agora = pygame.time.get_ticks()
        if agora - self.timers['radial'] > self.cadencias['radial']:
            self.timers['radial'] = agora
            num_tiros = 12 + self.nivel
            for i in range(num_tiros):
                angulo = (360 / num_tiros) * i
                tiro = TiroBoss(self.rect.centerx, self.rect.centery, angulo)
                todos_sprites.add(tiro)
                grupo_tiros_inimigos.add(tiro)
        if agora - self.timers['mira'] > self.cadencias['mira']:
            self.timers['mira'] = agora
            if self.jogadores_vivos:
                alvo = random.choice(self.jogadores_vivos)
                dx = alvo.rect.centerx - self.rect.centerx
                dy = alvo.rect.centery - self.rect.centery
                angulo = math.degrees(math.atan2(dy, dx))
                tiro = TiroBoss(self.rect.centerx, self.rect.centery, angulo)
                todos_sprites.add(tiro)
                grupo_tiros_inimigos.add(tiro)

# --- Classes de UI e Funções de Desenho ---
class Botao:
    def __init__(self, x, y, largura, altura, texto, cor_texto=BRANCO, cor_fundo=CINZA_ESCURO, cor_hover=AZUL):
        self.rect = pygame.Rect(x, y, largura, altura)
        self.texto = texto
        self.cor_texto = cor_texto
        self.cor_fundo = cor_fundo
        self.cor_hover = cor_hover
        self.fonte = pygame.font.Font(None, 30)
        self.ativo = True
    def desenhar(self, superficie):
        if not self.ativo: return
        mouse_pos = pygame.mouse.get_pos()
        cor_atual = self.cor_hover if self.rect.collidepoint(mouse_pos) else self.cor_fundo
        pygame.draw.rect(superficie, cor_atual, self.rect, border_radius=5)
        desenhar_texto(self.texto, self.fonte, self.cor_texto, superficie, self.rect.centerx, self.rect.centery, center=True)
    def foi_clicado(self, evento):
        if not self.ativo: return False
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            return self.rect.collidepoint(evento.pos)
        return False

def desenhar_texto(texto, fonte, cor, superficie, x, y, center=False):
    textobj = fonte.render(texto, True, cor)
    textrect = textobj.get_rect()
    if center: textrect.center = (x, y)
    else: textrect.topleft = (x, y)
    superficie.blit(textobj, textrect)

def desenhar_barra_vida(superficie, x, y, vida_atual, vida_maxima, cor, largura, altura):
    if vida_atual < 0: vida_atual = 0
    ratio = vida_atual / vida_maxima
    pygame.draw.rect(superficie, CINZA_ESCURO, (x - 2, y - 2, largura + 4, altura + 4))
    pygame.draw.rect(superficie, VERMELHO, (x, y, largura, altura))
    pygame.draw.rect(superficie, VERDE, (x, y, largura * ratio, altura))

def desenhar_barra_calor(superficie, x, y, calor_atual, calor_maximo, largura, altura, superaquecido):
    ratio = calor_atual / calor_maximo
    cor_barra = LARANJA if not superaquecido else VERMELHO
    if superaquecido and int(pygame.time.get_ticks() / 200) % 2 == 0:
        cor_barra = BRANCO
    pygame.draw.rect(superficie, CINZA_ESCURO, (x, y, largura, altura))
    pygame.draw.rect(superficie, cor_barra, (x, y, largura * ratio, altura))
    pygame.draw.rect(superficie, BRANCO, (x, y, largura, altura), 2)

# --- Telas do Jogo ---
def tela_menu():
    fonte_titulo = pygame.font.Font(None, 100)
    fonte_opcao = pygame.font.Font(None, 60)
    while True:
        tela.fill(PRETO)
        desenhar_texto("ALEXANDRE, O REI", fonte_titulo, BRANCO, tela, largura_tela / 2, altura_tela / 4, center=True)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        botao_1p = pygame.Rect(largura_tela / 2 - 150, altura_tela / 2 - 50, 300, 60)
        botao_2p = pygame.Rect(largura_tela / 2 - 150, altura_tela / 2 + 30, 300, 60)
        botao_sair = pygame.Rect(largura_tela / 2 - 150, altura_tela / 2 + 110, 300, 60)
        for botao, texto in [(botao_1p, "1 Jogador"), (botao_2p, "2 Jogadores"), (botao_sair, "Sair")]:
            if botao.collidepoint((mouse_x, mouse_y)):
                pygame.draw.rect(tela, AZUL, botao)
            else:
                pygame.draw.rect(tela, BRANCO, botao, 3)
            desenhar_texto(texto, fonte_opcao, BRANCO, tela, botao.centerx, botao.centery, center=True)
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if botao_1p.collidepoint((mouse_x, mouse_y)): return 1
                if botao_2p.collidepoint((mouse_x, mouse_y)): return 2
                if botao_sair.collidepoint((mouse_x, mouse_y)):
                    pygame.quit()
                    sys.exit()
        pygame.display.update()
        relogio.tick(FPS)

def tela_pausa():
    fonte_titulo = pygame.font.Font(None, 80)
    fonte_opcao = pygame.font.Font(None, 50)
    overlay = pygame.Surface((largura_tela, altura_tela), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))
    tela.blit(overlay, (0, 0))
    desenhar_texto("PAUSADO", fonte_titulo, BRANCO, tela, largura_tela / 2, altura_tela / 4, center=True)
    while True:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        botao_continuar = pygame.Rect(largura_tela / 2 - 150, altura_tela / 2 - 50, 300, 50)
        botao_reiniciar = pygame.Rect(largura_tela / 2 - 150, altura_tela / 2 + 20, 300, 50)
        botao_sair_menu = pygame.Rect(largura_tela / 2 - 150, altura_tela / 2 + 90, 300, 50)
        for botao, texto in [(botao_continuar, "Continuar"), (botao_reiniciar, "Reiniciar Fase"), (botao_sair_menu, "Sair para o Menu")]:
            if botao.collidepoint((mouse_x, mouse_y)):
                pygame.draw.rect(tela, AZUL, botao)
            else:
                pygame.draw.rect(tela, BRANCO, botao, 2)
            desenhar_texto(texto, fonte_opcao, BRANCO, tela, botao.centerx, botao.centery, center=True)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: return "CONTINUAR"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if botao_continuar.collidepoint((mouse_x, mouse_y)): return "CONTINUAR"
                if botao_reiniciar.collidepoint((mouse_x, mouse_y)): return "REINICIAR"
                if botao_sair_menu.collidepoint((mouse_x, mouse_y)): return "MENU"
        pygame.display.update()
        relogio.tick(FPS)

def tela_se_fudeu(nivel):
    fonte_titulo = pygame.font.Font(None, 150)
    fonte_sub = pygame.font.Font(None, 70)
    tela.fill(PRETO)
    desenhar_texto("SE FUDEU", fonte_titulo, VERMELHO, tela, largura_tela / 2, altura_tela / 3, center=True)
    desenhar_texto(f"Você morreu na Fase {nivel}", fonte_sub, BRANCO, tela, largura_tela / 2, altura_tela / 2, center=True)
    botao_menu = Botao(largura_tela / 2 - 150, altura_tela * 0.6, 300, 60, "Voltar ao Menu")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if botao_menu.foi_clicado(event): return
        botao_menu.desenhar(tela)
        pygame.display.update()
        relogio.tick(FPS)

def tela_upgrade(jogadores_vivos, jogadores_mortos):
    custos = {'velocidade': 50, 'dano': 75, 'cadencia': 100, 'reviver': 200}
    fonte_titulo = pygame.font.Font(None, 60)
    fonte_normal = pygame.font.Font(None, 30)
    botoes_por_jogador = {}
    todos_os_jogadores = sorted(jogadores_vivos + jogadores_mortos, key=lambda j: j.numero_jogador)
    espaco_entre_jogadores = largura_tela / (len(todos_os_jogadores) + 1)
    for i, jogador in enumerate(todos_os_jogadores):
        x_base = espaco_entre_jogadores * (i + 1)
        botoes_por_jogador[jogador.numero_jogador] = {
            'velocidade': Botao(x_base - 100, 200, 200, 40, f"Velocidade (+${custos['velocidade']})"),
            'dano': Botao(x_base - 100, 250, 200, 40, f"Dano (+${custos['dano']})"),
            'cadencia': Botao(x_base - 100, 300, 200, 40, f"Cadência (+${custos['cadencia']})"),
            'cor': Botao(x_base - 100, 350, 200, 40, "Mudar Cor")
        }
    botao_reviver = None
    if num_jogadores == 2 and jogadores_vivos and jogadores_mortos:
        jogador_vivo = jogadores_vivos[0]
        jogador_morto = jogadores_mortos[0]
        botao_reviver = Botao(largura_tela / 2 - 125, altura_tela - 200, 250, 50, f"Reviver P{jogador_morto.numero_jogador} (${custos['reviver']})")
    botao_continuar = Botao(largura_tela / 2 - 100, altura_tela - 100, 200, 50, "Próxima Fase")
    rodando_upgrade = True
    while rodando_upgrade:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if botao_continuar.foi_clicado(event): rodando_upgrade = False
            if botao_reviver and botao_reviver.foi_clicado(event):
                if jogador_vivo.dinheiro >= custos['reviver']:
                    jogador_vivo.dinheiro -= custos['reviver']
                    jogador_morto.reset_stats()
                    jogadores_vivos.append(jogador_morto)
                    jogadores_mortos.remove(jogador_morto)
                    botao_reviver.ativo = False
            for j in jogadores_vivos:
                botoes = botoes_por_jogador[j.numero_jogador]
                if botoes['velocidade'].foi_clicado(event) and j.dinheiro >= custos['velocidade']:
                    j.dinheiro -= custos['velocidade']; j.nivel_velocidade += 1; j.velocidade = j.velocidade_base + j.nivel_velocidade
                if botoes['dano'].foi_clicado(event) and j.dinheiro >= custos['dano']:
                    j.dinheiro -= custos['dano']; j.nivel_dano += 1; j.dano_tiro = j.dano_tiro_base + j.nivel_dano * 5
                if botoes['cadencia'].foi_clicado(event) and j.dinheiro >= custos['cadencia']:
                    j.dinheiro -= custos['cadencia']; j.nivel_cadencia += 1; j.cadencia_tiro = max(50, j.cadencia_tiro_base - j.nivel_cadencia * 15)
                if botoes['cor'].foi_clicado(event):
                    j.cor_atual_index = (j.cor_atual_index + 1) % len(CORES_NAVE)
                    j.cor = CORES_NAVE[j.cor_atual_index]
                    j.atualizar_imagem()
        tela.fill(PRETO)
        desenhar_texto("LOJA DE UPGRADES", fonte_titulo, BRANCO, tela, largura_tela / 2, 50, center=True)
        for i, jogador in enumerate(todos_os_jogadores):
            x_base = espaco_entre_jogadores * (i + 1)
            status = "VIVO" if jogador in jogadores_vivos else "MORTO"
            cor_status = VERDE if status == "VIVO" else VERMELHO
            desenhar_texto(f"Jogador {jogador.numero_jogador}", fonte_titulo, jogador.cor, tela, x_base, 100, center=True)
            desenhar_texto(f"({status})", fonte_normal, cor_status, tela, x_base, 140, center=True)
            if status == "VIVO":
                desenhar_texto(f"Dinheiro: ${jogador.dinheiro}", fonte_normal, AMARELO, tela, x_base, 170, center=True)
                botoes = botoes_por_jogador[jogador.numero_jogador]
                for b in botoes.values(): b.desenhar(tela)
                desenhar_texto(f"Vel: {jogador.nivel_velocidade} | Dano: {jogador.nivel_dano} | Cad: {jogador.nivel_cadencia}", fonte_normal, BRANCO, tela, x_base, 400, center=True)
        if botao_reviver: botao_reviver.desenhar(tela)
        botao_continuar.desenhar(tela)
        pygame.display.update()
        relogio.tick(FPS)

# --- Função Principal do Jogo ---
def loop_jogo():
    global num_jogadores, todos_sprites, grupo_jogadores, grupo_tiros_jogadores, grupo_inimigos, grupo_tiros_inimigos, grupo_boss
    estado_jogo = "JOGANDO"
    nivel_atual = 1
    controles_p1 = {'cima': pygame.K_w, 'baixo': pygame.K_s, 'esquerda': pygame.K_a, 'direita': pygame.K_d, 'tiro': pygame.K_v}
    controles_p2 = {'cima': pygame.K_UP, 'baixo': pygame.K_DOWN, 'esquerda': pygame.K_LEFT, 'direita': pygame.K_RIGHT, 'tiro': pygame.K_l}
    jogadores_config = [{'id': 1, 'cor': AZUL, 'controles': controles_p1}, {'id': 2, 'cor': AMARELO, 'controles': controles_p2}]
    jogadores_em_partida = [Nave(0, 0, p['cor'], p['controles'], p['id']) for i, p in enumerate(jogadores_config) if i < num_jogadores]

    def preparar_fase(nivel, jogadores_atuais):
        nonlocal inimigos_derrotados, estado_fase
        inimigos_derrotados = 0
        estado_fase = "INIMIGOS"
        inimigos_para_derrotar = 10 + (nivel - 1) * 2
        for sprite in todos_sprites:
            if not isinstance(sprite, Nave): sprite.kill()
        for i, jogador in enumerate(jogadores_atuais):
            jogador.rect.center = (100, altura_tela / 2 + ((i * 100) - 50 if len(jogadores_atuais) > 1 else 0))
            jogador.vida = jogador.vida_maxima
            todos_sprites.add(jogador)
            grupo_jogadores.add(jogador)
        return inimigos_para_derrotar

    todos_sprites = pygame.sprite.Group(); grupo_jogadores = pygame.sprite.Group(); grupo_tiros_jogadores = pygame.sprite.Group()
    grupo_inimigos = pygame.sprite.Group(); grupo_tiros_inimigos = pygame.sprite.Group(); grupo_boss = pygame.sprite.Group()
    inimigos_para_derrotar = preparar_fase(nivel_atual, jogadores_em_partida)
    inimigos_derrotados = 0
    ultimo_spawn_inimigo = pygame.time.get_ticks()
    rodando = True
    while rodando:
        dt = relogio.tick(FPS) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                acao = tela_pausa()
                if acao == "REINICIAR":
                    loop_jogo()
                    return
                if acao == "MENU": return

        if not grupo_jogadores:
            tela_se_fudeu(nivel_atual)
            return

        if estado_jogo == "JOGANDO":
            if estado_fase == "INIMIGOS":
                agora = pygame.time.get_ticks()
                if agora - ultimo_spawn_inimigo > 2000 and len(grupo_inimigos) < 8:
                    ultimo_spawn_inimigo = agora
                    inimigo = Inimigo()
                    todos_sprites.add(inimigo)
                    grupo_inimigos.add(inimigo)
                if inimigos_derrotados >= inimigos_para_derrotar:
                    estado_fase = "BOSS"
                    for inimigo in grupo_inimigos: inimigo.kill()
                    boss = Boss(nivel_atual, list(grupo_jogadores))
                    todos_sprites.add(boss)
                    grupo_boss.add(boss)
            
            todos_sprites.update(dt)
            
            acertos_inimigos = pygame.sprite.groupcollide(grupo_inimigos, grupo_tiros_jogadores, False, True)
            for inimigo, tiros in acertos_inimigos.items():
                inimigo.vida -= tiros[0].dano
                if inimigo.vida <= 0:
                    inimigo.kill()
                    inimigos_derrotados += 1
                    for j in grupo_jogadores: j.dinheiro += 10
            
            acertos_boss = pygame.sprite.groupcollide(grupo_boss, grupo_tiros_jogadores, False, True)
            for boss, tiros in acertos_boss.items():
                boss.vida -= tiros[0].dano
                if boss.vida <= 0:
                    boss.kill()
                    nivel_atual += 1
                    for j in grupo_jogadores: j.dinheiro += 100 * (nivel_atual - 1)
                    estado_jogo = "UPGRADE"
            
            acertos_jogadores = pygame.sprite.groupcollide(grupo_jogadores, grupo_tiros_inimigos, False, True)
            for jogador, tiros in acertos_jogadores.items():
                jogador.receber_dano(tiros[0].dano)

            colisoes_corpo = pygame.sprite.groupcollide(grupo_jogadores, grupo_inimigos, False, True)
            for jogador, inimigos_colididos in colisoes_corpo.items():
                jogador.receber_dano(DANO_COLISAO * len(inimigos_colididos))
                inimigos_derrotados += len(inimigos_colididos)
                for j in grupo_jogadores: j.dinheiro += 10 * len(inimigos_colididos)

        elif estado_jogo == "UPGRADE":
            jogadores_vivos = list(grupo_jogadores)
            jogadores_mortos = [p for p in jogadores_em_partida if p not in jogadores_vivos]
            tela_upgrade(jogadores_vivos, jogadores_mortos)
            jogadores_em_partida = sorted(jogadores_vivos + jogadores_mortos, key=lambda j: j.numero_jogador)
            inimigos_para_derrotar = preparar_fase(nivel_atual, jogadores_em_partida)
            estado_jogo = "JOGANDO"

        tela.fill(PRETO)
        todos_sprites.draw(tela)
        fonte_hud = pygame.font.Font(None, 40)
        desenhar_texto(f"Fase: {nivel_atual}", fonte_hud, BRANCO, tela, largura_tela / 2, 20, center=True)
        y_offset = 0
        for jogador in sorted(list(grupo_jogadores), key=lambda j: j.numero_jogador):
            y_base = 20 + y_offset
            desenhar_texto(f"P{jogador.numero_jogador}", fonte_hud, jogador.cor, tela, 20, y_base)
            desenhar_barra_vida(tela, 70, y_base, jogador.vida, jogador.vida_maxima, jogador.cor, 200, 15)
            desenhar_barra_calor(tela, 70, y_base + 20, jogador.calor_atual, jogador.calor_maximo, 200, 10, jogador.superaquecido)
            desenhar_texto(f"$:{jogador.dinheiro}", fonte_hud, AMARELO, tela, 20, y_base + 35)
            y_offset += 80
        
        if estado_fase == "BOSS" and grupo_boss:
            boss = grupo_boss.sprites()[0]
            desenhar_barra_vida(tela, largura_tela / 2 - 200, 50, boss.vida, boss.vida_maxima, VERMELHO, 400, 25)
            
        pygame.display.flip()

# --- Gerenciador Principal ---
if __name__ == "__main__":
    while True:
        num_jogadores = tela_menu()
        loop_jogo()