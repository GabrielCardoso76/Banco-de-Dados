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
pygame.display.set_caption("Batalha Espacial: Ataque Total")

# --- Cores e Constantes ---
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (50, 50, 255)
AMARELO = (255, 255, 0)
CINZA_ESCURO = (40, 40, 40)
LARANJA = (255, 165, 0)
DANO_COLISAO = 40 # <--- NOVO: Dano por colisão corporal

# --- Relógio do Jogo ---
relogio = pygame.time.Clock()
FPS = 60

# --- Classe do Jogador (Nave) ---
class Nave(pygame.sprite.Sprite):
    def __init__(self, x, y, cor, controles):
        super().__init__()
        self.imagem_original = pygame.Surface((50, 30), pygame.SRCALPHA)
        pygame.draw.polygon(self.imagem_original, cor, [(50, 15), (0, 0), (0, 30)])
        self.image = self.imagem_original
        self.rect = self.image.get_rect(center=(x, y))
        self.cor = cor
        self.controles = controles
        self.velocidade = 7
        self.velocidade_tiro = 15
        self.dano_tiro = 15
        self.vida = 100
        self.vida_maxima = 100
        self.dinheiro = 0
        self.ultimo_tiro = pygame.time.get_ticks()
        self.cadencia_tiro = 200

    def update(self):
        teclas = pygame.key.get_pressed()
        if teclas[self.controles['esquerda']] and self.rect.left > 0: self.rect.x -= self.velocidade
        if teclas[self.controles['direita']] and self.rect.right < largura_tela: self.rect.x += self.velocidade
        if teclas[self.controles['cima']] and self.rect.top > 0: self.rect.y -= self.velocidade
        if teclas[self.controles['baixo']] and self.rect.bottom < altura_tela: self.rect.y += self.velocidade
        if teclas[self.controles['tiro']]: self.atirar()

    def atirar(self):
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_tiro > self.cadencia_tiro:
            self.ultimo_tiro = agora
            tiro = TiroJogador(self.rect.right, self.rect.centery, self.velocidade_tiro, self.dano_tiro, self.cor)
            todos_sprites.add(tiro)
            grupo_tiros_jogadores.add(tiro)
    
    def receber_dano(self, dano):
        self.vida -= dano
        if self.vida <= 0:
            self.vida = 0
            self.kill()

# ... (Classes de Tiros, Inimigo e Boss permanecem as mesmas) ...
class TiroJogador(pygame.sprite.Sprite):
    def __init__(self, x, y, velocidade, dano, cor):
        super().__init__()
        self.image = pygame.Surface((15, 4))
        self.image.fill(cor)
        self.rect = self.image.get_rect(midleft=(x, y))
        self.velocidade = velocidade
        self.dano = dano

    def update(self):
        self.rect.x += self.velocidade
        if self.rect.left > largura_tela: self.kill()

class TiroInimigo(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((12, 4))
        self.image.fill(LARANJA)
        self.rect = self.image.get_rect(midright=(x, y))
        self.velocidade_x = -8
        self.dano = 10

    def update(self):
        self.rect.x += self.velocidade_x
        if self.rect.right < 0: self.kill()

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
    
    def update(self):
        self.rect.x += self.velocidade_x
        self.rect.y += self.velocidade_y
        if self.rect.bottom < 0 or self.rect.top > altura_tela or self.rect.right < 0 or self.rect.left > largura_tela:
            self.kill()

class Inimigo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.imagem_original = pygame.Surface((40, 35), pygame.SRCALPHA)
        pygame.draw.polygon(self.imagem_original, VERMELHO, [(0, 17.5), (40, 0), (40, 35)])
        self.image = self.imagem_original
        self.rect = self.image.get_rect(center=(largura_tela + 50, random.randint(50, altura_tela - 50)))
        self.velocidade_x = random.randint(2, 5)
        self.vida = 30
        self.ultimo_tiro = pygame.time.get_ticks()
        self.cadencia_tiro = 2500

    def update(self):
        self.rect.x -= self.velocidade_x
        if self.rect.right < 0: self.kill()
        self.atirar()

    def atirar(self):
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_tiro > self.cadencia_tiro:
            self.ultimo_tiro = agora
            tiro = TiroInimigo(self.rect.left, self.rect.centery)
            todos_sprites.add(tiro)
            grupo_tiros_inimigos.add(tiro)

class Boss(pygame.sprite.Sprite):
    def __init__(self, nivel):
        super().__init__()
        largura_boss = 120 + nivel * 15
        altura_boss = 100 + nivel * 15
        self.image = pygame.Surface((largura_boss, altura_boss), pygame.SRCALPHA)
        pygame.draw.rect(self.image, VERMELHO, (0, 0, largura_boss, altura_boss), border_radius=15)
        self.rect = self.image.get_rect(center=(largura_tela - 100, altura_tela / 2))
        self.vida = 1000 + nivel * 200
        self.vida_maxima = self.vida
        self.velocidade_y = 2 + nivel * 0.5
        self.ultimo_tiro_radial = pygame.time.get_ticks()
        self.cadencia_radial = 1500
    
    def update(self):
        self.rect.y += self.velocidade_y
        if self.rect.top < 0:
            self.rect.top = 0
            self.velocidade_y *= -1
        if self.rect.bottom > altura_tela:
            self.rect.bottom = altura_tela
            self.velocidade_y *= -1
        self.atirar()

    def atirar(self):
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_tiro_radial > self.cadencia_radial:
            self.ultimo_tiro_radial = agora
            for angulo in range(0, 360, 30):
                tiro = TiroBoss(self.rect.centerx, self.rect.centery, angulo)
                todos_sprites.add(tiro)
                grupo_tiros_inimigos.add(tiro)


# ... (Funções de Interface e Telas permanecem as mesmas) ...
def desenhar_texto(texto, fonte, cor, superficie, x, y, center=False):
    textobj = fonte.render(texto, True, cor)
    textrect = textobj.get_rect()
    if center: textrect.center = (x, y)
    else: textrect.topleft = (x, y)
    superficie.blit(textobj, textrect)

def desenhar_barra_vida(superficie, x, y, vida_atual, vida_maxima, cor, largura, altura):
    if vida_atual < 0: vida_atual = 0
    ratio = vida_atual / vida_maxima
    pygame.draw.rect(superficie, CINZA_ESCURO, (x-2, y-2, largura+4, altura+4))
    pygame.draw.rect(superficie, VERMELHO, (x, y, largura, altura))
    pygame.draw.rect(superficie, VERDE, (x, y, largura * ratio, altura))

def tela_menu():
    fonte_titulo = pygame.font.Font(None, 100)
    fonte_opcao = pygame.font.Font(None, 60)
    
    while True:
        tela.fill(PRETO)
        desenhar_texto("BATALHA ESPACIAL", fonte_titulo, BRANCO, tela, largura_tela/2, altura_tela/4, center=True)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        botao_1p = pygame.Rect(largura_tela/2 - 150, altura_tela/2 - 50, 300, 60)
        botao_2p = pygame.Rect(largura_tela/2 - 150, altura_tela/2 + 30, 300, 60)
        botao_sair = pygame.Rect(largura_tela/2 - 150, altura_tela/2 + 110, 300, 60)
        for botao, texto in [(botao_1p, "1 Jogador"), (botao_2p, "2 Jogadores"), (botao_sair, "Sair")]:
            if botao.collidepoint((mouse_x, mouse_y)): pygame.draw.rect(tela, AZUL, botao)
            else: pygame.draw.rect(tela, BRANCO, botao, 3)
            desenhar_texto(texto, fonte_opcao, BRANCO, tela, botao.centerx, botao.centery, center=True)
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE): pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if botao_1p.collidepoint((mouse_x, mouse_y)): return 1
                if botao_2p.collidepoint((mouse_x, mouse_y)): return 2
                if botao_sair.collidepoint((mouse_x, mouse_y)): pygame.quit(); sys.exit()
        pygame.display.update()
        relogio.tick(FPS)

def tela_pausa():
    fonte_titulo = pygame.font.Font(None, 80)
    fonte_opcao = pygame.font.Font(None, 50)
    overlay = pygame.Surface((largura_tela, altura_tela), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))
    tela.blit(overlay, (0, 0))
    desenhar_texto("PAUSADO", fonte_titulo, BRANCO, tela, largura_tela/2, altura_tela/4, center=True)
    while True:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        botao_continuar = pygame.Rect(largura_tela/2 - 150, altura_tela/2 - 50, 300, 50)
        botao_reiniciar = pygame.Rect(largura_tela/2 - 150, altura_tela/2 + 20, 300, 50)
        botao_sair_menu = pygame.Rect(largura_tela/2 - 150, altura_tela/2 + 90, 300, 50)
        for botao, texto in [(botao_continuar, "Continuar"), (botao_reiniciar, "Reiniciar Fase"), (botao_sair_menu, "Sair para o Menu")]:
            if botao.collidepoint((mouse_x, mouse_y)): pygame.draw.rect(tela, AZUL, botao)
            else: pygame.draw.rect(tela, BRANCO, botao, 2)
            desenhar_texto(texto, fonte_opcao, BRANCO, tela, botao.centerx, botao.centery, center=True)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: return "CONTINUAR"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if botao_continuar.collidepoint((mouse_x, mouse_y)): return "CONTINUAR"
                if botao_reiniciar.collidepoint((mouse_x, mouse_y)): return "REINICIAR"
                if botao_sair_menu.collidepoint((mouse_x, mouse_y)): return "MENU"
        pygame.display.update()
        relogio.tick(FPS)

def tela_fim_de_jogo():
    fonte_titulo = pygame.font.Font(None, 120)
    fonte_opcao = pygame.font.Font(None, 60)
    tela.fill(PRETO)
    desenhar_texto("FIM DE JOGO", fonte_titulo, VERMELHO, tela, largura_tela/2, altura_tela/3, center=True)
    while True:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        botao_menu = pygame.Rect(largura_tela/2 - 150, altura_tela/2, 300, 60)
        if botao_menu.collidepoint((mouse_x, mouse_y)): pygame.draw.rect(tela, AZUL, botao_menu)
        else: pygame.draw.rect(tela, BRANCO, botao_menu, 3)
        desenhar_texto("Voltar ao Menu", fonte_opcao, BRANCO, tela, botao_menu.centerx, botao_menu.centery, center=True)
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE): pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if botao_menu.collidepoint((mouse_x, mouse_y)): return
        pygame.display.update()
        relogio.tick(FPS)

# --- Função Principal do Jogo ---
def loop_jogo():
    global num_jogadores, todos_sprites, grupo_jogadores, grupo_tiros_jogadores, grupo_inimigos, grupo_tiros_inimigos, grupo_boss
    # ... (código da função loop_jogo com as correções)
    nivel_atual = 1
    inimigos_para_derrotar = 10
    inimigos_derrotados = 0
    estado_fase = "INIMIGOS"

    controles_p1 = {'cima': pygame.K_w, 'baixo': pygame.K_s, 'esquerda': pygame.K_a, 'direita': pygame.K_d, 'tiro': pygame.K_v}
    controles_p2 = {'cima': pygame.K_UP, 'baixo': pygame.K_DOWN, 'esquerda': pygame.K_LEFT, 'direita': pygame.K_RIGHT, 'tiro': pygame.K_l}

    def resetar_fase():
        nonlocal inimigos_derrotados, estado_fase
        for grupo in [todos_sprites, grupo_jogadores, grupo_tiros_jogadores, grupo_inimigos, grupo_tiros_inimigos, grupo_boss]:
            grupo.empty()

        jogador1 = Nave(100, altura_tela / 2 - 50, AZUL, controles_p1)
        todos_sprites.add(jogador1)
        grupo_jogadores.add(jogador1)
        jogadores_vivos = [jogador1]
        
        if num_jogadores == 2:
            jogador2 = Nave(100, altura_tela / 2 + 50, AMARELO, controles_p2)
            todos_sprites.add(jogador2)
            grupo_jogadores.add(jogador2)
            jogadores_vivos.append(jogador2)
        
        inimigos_derrotados = 0
        estado_fase = "INIMIGOS"
        return jogadores_vivos

    todos_sprites = pygame.sprite.Group()
    grupo_jogadores = pygame.sprite.Group()
    grupo_tiros_jogadores = pygame.sprite.Group()
    grupo_inimigos = pygame.sprite.Group()
    grupo_tiros_inimigos = pygame.sprite.Group()
    grupo_boss = pygame.sprite.Group()

    jogadores_vivos = resetar_fase()
    
    ultimo_spawn_inimigo = pygame.time.get_ticks()
    intervalo_spawn = 2000

    rodando = True
    while rodando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    acao_pausa = tela_pausa()
                    if acao_pausa == "REINICIAR": jogadores_vivos = resetar_fase()
                    elif acao_pausa == "MENU": rodando = False

        if not grupo_jogadores:
            tela_fim_de_jogo()
            rodando = False
            continue

        if estado_fase == "INIMIGOS":
            agora = pygame.time.get_ticks()
            if agora - ultimo_spawn_inimigo > intervalo_spawn and len(grupo_inimigos) < 8:
                ultimo_spawn_inimigo = agora
                inimigo = Inimigo()
                todos_sprites.add(inimigo)
                grupo_inimigos.add(inimigo)
            
            if inimigos_derrotados >= inimigos_para_derrotar:
                estado_fase = "BOSS"
                for inimigo in grupo_inimigos: inimigo.kill()
                boss = Boss(nivel_atual)
                todos_sprites.add(boss)
                grupo_boss.add(boss)
        
        todos_sprites.update()
        
        # --- Seção de Colisões ---
        # Tiro do Jogador em Inimigos
        acertos_inimigos = pygame.sprite.groupcollide(grupo_inimigos, grupo_tiros_jogadores, False, True)
        for inimigo, tiros in acertos_inimigos.items():
            inimigo.vida -= tiros[0].dano
            if inimigo.vida <= 0:
                inimigo.kill()
                inimigos_derrotados += 1
                for jogador in grupo_jogadores: jogador.dinheiro += 10

        # Tiro do Jogador no Boss
        acertos_boss = pygame.sprite.groupcollide(grupo_boss, grupo_tiros_jogadores, False, True)
        for boss, tiros in acertos_boss.items():
            boss.vida -= tiros[0].dano
            if boss.vida <= 0:
                boss.kill()
                nivel_atual += 1
                inimigos_derrotados = 0
                inimigos_para_derrotar += 5
                estado_fase = "INIMIGOS"
                for jogador in grupo_jogadores: jogador.dinheiro += 100 * (nivel_atual - 1)
        
        # Tiro Inimigo no Jogador
        acertos_jogadores_tiros = pygame.sprite.groupcollide(grupo_jogadores, grupo_tiros_inimigos, False, True)
        for jogador, tiros in acertos_jogadores_tiros.items():
            jogador.receber_dano(tiros[0].dano)

        # <--- NOVO: COLISÃO DE NAVES --- >
        # Colisão corporal: Jogador com Inimigo
        colisoes_corporais = pygame.sprite.groupcollide(grupo_jogadores, grupo_inimigos, False, True)
        if colisoes_corporais:
            for jogador, inimigos_atingidos in colisoes_corporais.items():
                jogador.receber_dano(DANO_COLISAO * len(inimigos_atingidos))
                inimigos_derrotados += len(inimigos_atingidos)
                # Adiciona dinheiro pela destruição do inimigo na colisão
                for jogador_vivo in grupo_jogadores:
                    jogador_vivo.dinheiro += 10 * len(inimigos_atingidos)


        # --- Seção de Desenho ---
        tela.fill(PRETO)
        todos_sprites.draw(tela)

        fonte_hud = pygame.font.Font(None, 40)
        y_offset = 0
        for i, jogador in enumerate(jogadores_vivos):
            cor_hud = jogador.cor
            desenhar_texto(f"P{i+1}", fonte_hud, cor_hud, tela, 20, 20 + y_offset)
            desenhar_barra_vida(tela, 70, 20 + y_offset, jogador.vida, jogador.vida_maxima, cor_hud, 200, 20)
            desenhar_texto(f"$:{jogador.dinheiro}", fonte_hud, AMARELO, tela, 20, 45 + y_offset)
            y_offset += 70
        
        if estado_fase == "INIMIGOS":
            desenhar_texto(f"Inimigos: {inimigos_derrotados}/{inimigos_para_derrotar}", fonte_hud, BRANCO, tela, largura_tela/2, 20, center=True)
        
        # <--- CORRIGIDO: Desenho da vida do Boss --- >
        elif estado_fase == "BOSS" and grupo_boss: # Checa se o grupo não está vazio
            boss = grupo_boss.sprites()[0] # Pega o sprite do boss de dentro do grupo
            desenhar_texto("CHEFE", fonte_hud, VERMELHO, tela, largura_tela/2, 20, center=True)
            desenhar_barra_vida(tela, largura_tela/2 - 200, 50, boss.vida, boss.vida_maxima, VERMELHO, 400, 25)
            
        pygame.display.flip()
        relogio.tick(FPS)

# --- Gerenciador Principal do Jogo ---
if __name__ == "__main__":
    while True:
        num_jogadores = tela_menu()
        loop_jogo()