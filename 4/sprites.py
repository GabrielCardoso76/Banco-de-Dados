import pygame
import random
import math
from settings import *

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

        self.vida = 100
        self.vida_maxima = 100
        self.dinheiro = 0
        self.ultimo_tiro = pygame.time.get_ticks()

        self.curas_disponiveis = 1
        self.bombas_disponiveis = 1

        self.velocidade_base = 7
        self.dano_tiro_base = 15
        self.cadencia_tiro_base = 200
        self.nivel_velocidade = 0; self.nivel_dano = 0; self.nivel_cadencia = 0
        self.nivel_tipo_tiro = 0; self.nivel_resfriamento = 0
        self.velocidade = self.velocidade_base; self.dano_tiro = self.dano_tiro_base; self.cadencia_tiro = self.cadencia_tiro_base

        self.calor_atual = 0; self.calor_maximo = 100
        self.taxa_aumento_calor_base = 8; self.taxa_resfriamento_base = 12
        self.taxa_aumento_calor = self.taxa_aumento_calor_base; self.taxa_resfriamento = self.taxa_resfriamento_base
        self.superaquecido = False; self.tempo_superaquecimento = 0; self.duracao_cooldown = 3000

    def atualizar_imagem(self):
        self.imagem_original.fill((0, 0, 0, 0))
        pygame.draw.polygon(self.imagem_original, self.cor, [(50, 15), (0, 0), (0, 30)])
        self.image = self.imagem_original

    def update(self, dt, game, grupos_de_sprites):
        teclas = pygame.key.get_pressed()
        if teclas[self.controles['esquerda']] and self.rect.left > 0: self.rect.x -= self.velocidade
        if teclas[self.controles['direita']] and self.rect.right < game.LARGURA_TELA: self.rect.x += self.velocidade
        if teclas[self.controles['cima']] and self.rect.top > 0: self.rect.y -= self.velocidade
        if teclas[self.controles['baixo']] and self.rect.bottom < game.ALTURA_TELA: self.rect.y += self.velocidade
        
        if teclas[self.controles['tiro']]: self.atirar(grupos_de_sprites)

        if not self.superaquecido and self.calor_atual > 0:
            self.calor_atual -= self.taxa_resfriamento * dt
            if self.calor_atual < 0: self.calor_atual = 0
        
        if self.superaquecido:
            if pygame.time.get_ticks() - self.tempo_superaquecimento > self.duracao_cooldown:
                self.superaquecido = False
                self.calor_atual = 0

    def atirar(self, grupos_de_sprites):
        if self.superaquecido: return
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_tiro > self.cadencia_tiro:
            self.ultimo_tiro = agora
            if self.nivel_tipo_tiro == 0:
                tiro = TiroJogador(self.rect.right, self.rect.centery, self.dano_tiro, self.cor)
                grupos_de_sprites['todos'].add(tiro)
                grupos_de_sprites['tiros_jogadores'].add(tiro)
            else:
                for angulo in [-15, 0, 15]:
                    tiro = TiroJogador(self.rect.right, self.rect.centery, self.dano_tiro, self.cor, angulo)
                    grupos_de_sprites['todos'].add(tiro)
                    grupos_de_sprites['tiros_jogadores'].add(tiro)
            
            self.calor_atual += self.taxa_aumento_calor
            if self.calor_atual >= self.calor_maximo:
                self.calor_atual = self.calor_maximo
                self.superaquecido = True
                self.tempo_superaquecimento = pygame.time.get_ticks()

    def usar_cura(self):
        if self.curas_disponiveis > 0 and self.vida < self.vida_maxima:
            self.vida += 50
            if self.vida > self.vida_maxima: self.vida = self.vida_maxima
            self.curas_disponiveis -= 1

    def usar_bomba(self, grupos_de_sprites):
        if self.bombas_disponiveis > 0:
            bomba = Bomba(self.rect.right, self.rect.centery)
            grupos_de_sprites['todos'].add(bomba)
            grupos_de_sprites['bombas'].add(bomba)
            self.bombas_disponiveis -= 1

    def receber_dano(self, dano):
        self.vida -= dano
        if self.vida <= 0:
            self.vida = 0
            self.kill()

    def reset_stats(self):
        self.nivel_velocidade = 0; self.nivel_dano = 0; self.nivel_cadencia = 0
        self.nivel_tipo_tiro = 0; self.nivel_resfriamento = 0
        self.velocidade = self.velocidade_base; self.dano_tiro = self.dano_tiro_base; self.cadencia_tiro = self.cadencia_tiro_base
        self.taxa_aumento_calor = self.taxa_aumento_calor_base; self.taxa_resfriamento = self.taxa_resfriamento_base

# --- Classes de Tiros e Consumíveis ---
class TiroJogador(pygame.sprite.Sprite):
    def __init__(self, x, y, dano, cor, angulo=0):
        super().__init__()
        self.image = pygame.Surface((15, 4), pygame.SRCALPHA)
        self.image.fill(cor)
        self.rect = self.image.get_rect(midleft=(x, y))
        self.velocidade = 15
        self.dano = dano
        radianos = math.radians(angulo)
        self.velocidade_x = math.cos(radianos) * self.velocidade
        self.velocidade_y = math.sin(radianos) * self.velocidade
    
    def update(self, dt, game, grupos_de_sprites):
        self.rect.x += self.velocidade_x
        self.rect.y += self.velocidade_y
        if not game.tela.get_rect().colliderect(self.rect):
            self.kill()

class TiroInimigo(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((12, 4))
        self.image.fill(LARANJA)
        self.rect = self.image.get_rect(midright=(x, y))
        self.velocidade_x = -8
        self.dano = 10

    def update(self, dt, game, grupos_de_sprites):
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

    def update(self, dt, game, grupos_de_sprites):
        self.rect.x += self.velocidade_x
        self.rect.y += self.velocidade_y
        if not game.tela.get_rect().colliderect(self.rect):
            self.kill()

class TiroTeleguiado(pygame.sprite.Sprite):
    def __init__(self, x, y, alvo, nivel):
        super().__init__()
        self.image = pygame.Surface((12, 12), pygame.SRCALPHA)
        pygame.draw.circle(self.image, ROXO, (6, 6), 6)
        pygame.draw.circle(self.image, VERMELHO, (6, 6), 3)
        self.rect = self.image.get_rect(center=(x, y))
        self.alvo = alvo
        self.velocidade = 5.5
        self.dano = 20
        self.tempo_de_vida = 3000 + (nivel * 500)
        self.criacao = pygame.time.get_ticks()

    def update(self, dt, game, grupos_de_sprites):
        if not self.alvo.alive() or (pygame.time.get_ticks() - self.criacao > self.tempo_de_vida):
            self.kill()
            return
        
        dx = self.alvo.rect.centerx - self.rect.centerx
        dy = self.alvo.rect.centery - self.rect.centery
        distancia = math.hypot(dx, dy)
        if distancia == 0:
            return
        
        dx, dy = dx / distancia, dy / distancia
        self.rect.x += dx * self.velocidade
        self.rect.y += dy * self.velocidade

class Bomba(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.circle(self.image, BRANCO, (10, 10), 10)
        pygame.draw.circle(self.image, CINZA_ESCURO, (10, 10), 6)
        self.rect = self.image.get_rect(center=(x, y))
        self.velocidade_x = 4

    def update(self, dt, game, grupos_de_sprites):
        self.rect.x += self.velocidade_x
        if self.rect.left > game.LARGURA_TELA:
            self.kill()

class Explosao(pygame.sprite.Sprite):
    def __init__(self, center):
        super().__init__()
        self.raio_max = 80
        self.duracao = 300
        self.criacao = pygame.time.get_ticks()
        self.image = pygame.Surface((self.raio_max * 2, self.raio_max * 2), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=center)

    def update(self, dt, game, grupos_de_sprites):
        agora = pygame.time.get_ticks()
        progresso = (agora - self.criacao) / self.duracao
        if progresso >= 1:
            self.kill()
            return
            
        raio_atual = int(self.raio_max * progresso)
        self.image.fill((0, 0, 0, 0))
        pygame.draw.circle(self.image, LARANJA, (self.raio_max, self.raio_max), raio_atual)

# --- Classes de Inimigos ---
class Inimigo(pygame.sprite.Sprite):
    def __init__(self, largura_tela, altura_tela):
        super().__init__()
        self.image = pygame.Surface((40, 35), pygame.SRCALPHA)
        pygame.draw.polygon(self.image, VERMELHO, [(0, 17.5), (40, 0), (40, 35)])
        self.rect = self.image.get_rect(center=(largura_tela + 50, random.randint(50, altura_tela - 50)))
        self.velocidade_x = random.randint(2, 5)
        self.vida = 30
        self.ultimo_tiro = pygame.time.get_ticks()
        self.cadencia_tiro = 2500

    def update(self, dt, game, grupos_de_sprites):
        self.rect.x -= self.velocidade_x
        if self.rect.right < 0:
            self.kill() # O dano é aplicado no loop principal
        self.atirar(grupos_de_sprites)

    def atirar(self, grupos_de_sprites):
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_tiro > self.cadencia_tiro:
            self.ultimo_tiro = agora
            tiro = TiroInimigo(self.rect.left, self.rect.centery)
            grupos_de_sprites['todos'].add(tiro)
            grupos_de_sprites['tiros_inimigos'].add(tiro)

class InimigoZigZag(Inimigo):
    def __init__(self, largura_tela, altura_tela):
        super().__init__(largura_tela, altura_tela)
        self.velocidade_y = random.choice([-3, 3])
    
    def update(self, dt, game, grupos_de_sprites):
        super().update(dt, game, grupos_de_sprites)
        self.rect.y += self.velocidade_y
        if self.rect.top < 0 or self.rect.bottom > game.ALTURA_TELA:
            self.velocidade_y *= -1

class InimigoAtiradorMulti(Inimigo):
    def atirar(self, grupos_de_sprites):
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_tiro > self.cadencia_tiro:
            self.ultimo_tiro = agora
            for angulo in [-165, 180, 195]:
                tiro = TiroBoss(self.rect.centerx, self.rect.centery, angulo)
                grupos_de_sprites['todos'].add(tiro)
                grupos_de_sprites['tiros_inimigos'].add(tiro)

# --- Classes dos Chefes ---
class BossBase(pygame.sprite.Sprite):
    def __init__(self, nivel, jogadores_vivos, largura_tela, altura_tela):
        super().__init__()
        self.jogadores_vivos = jogadores_vivos
        self.nivel = nivel
        self.vida = 1000 + nivel * 300
        self.vida_maxima = self.vida
        self.timers = {'aliado': pygame.time.get_ticks()}
        self.largura_tela = largura_tela
        self.altura_tela = altura_tela

    def update(self, dt, game, grupos_de_sprites):
        self.movimento()
        self.atirar(grupos_de_sprites)
        self.invocar_aliados(grupos_de_sprites)

    def movimento(self):
        pass
    def atirar(self, grupos_de_sprites):
        pass
    def invocar_aliados(self, grupos_de_sprites):
        agora = pygame.time.get_ticks()
        vida_ratio = self.vida / self.vida_maxima
        cadencia_aliado = 1500 + (vida_ratio * 4000)
        if agora - self.timers['aliado'] > cadencia_aliado:
            self.timers['aliado'] = agora
            inimigo = InimigoZigZag(self.largura_tela, self.altura_tela)
            grupos_de_sprites['todos'].add(inimigo)
            grupos_de_sprites['inimigos'].add(inimigo)

class BossQuadrado(BossBase):
    def __init__(self, nivel, jogadores_vivos, largura_tela, altura_tela):
        super().__init__(nivel, jogadores_vivos, largura_tela, altura_tela)
        self.image = pygame.Surface((120, 120))
        self.image.fill(VERMELHO)
        self.rect = self.image.get_rect(midright=(self.largura_tela - 20, self.altura_tela / 2))
        self.velocidade_y = 4 + nivel * 0.5
        self.timers['tiro_parede'] = pygame.time.get_ticks()
        self.cadencias = {'tiro_parede': 2500 - nivel * 100}

    def movimento(self):
        self.rect.y += self.velocidade_y
        if self.rect.top < 0:
            self.rect.top = 0
            self.velocidade_y *= -1
        if self.rect.bottom > self.altura_tela:
            self.rect.bottom = self.altura_tela
            self.velocidade_y *= -1

    def atirar(self, grupos_de_sprites):
        agora = pygame.time.get_ticks()
        if agora - self.timers['tiro_parede'] > self.cadencias['tiro_parede']:
            self.timers['tiro_parede'] = agora
            for i in range(10):
                tiro = TiroInimigo(self.rect.left, self.rect.top + i * 12)
                grupos_de_sprites['todos'].add(tiro)
                grupos_de_sprites['tiros_inimigos'].add(tiro)

class BossCirculo(BossBase):
    def __init__(self, nivel, jogadores_vivos, largura_tela, altura_tela):
        super().__init__(nivel, jogadores_vivos, largura_tela, altura_tela)
        self.image = pygame.Surface((130, 130), pygame.SRCALPHA)
        pygame.draw.circle(self.image, VERMELHO, (65, 65), 65)
        self.rect = self.image.get_rect(midright=(self.largura_tela - 20, self.altura_tela / 2))
        self.velocidade_x = 1 + nivel * 0.2
        self.velocidade_y = 2 + nivel * 0.5
        self.timers.update({'radial': 0, 'teleguiado': 0})
        self.cadencias = {'radial': 2000 - nivel * 150, 'teleguiado': 7000 - nivel * 300}

    def movimento(self):
        self.rect.y += self.velocidade_y
        self.rect.x -= self.velocidade_x
        if self.rect.top < 0:
            self.rect.top = 0
            self.velocidade_y *= -1
        if self.rect.bottom > self.altura_tela:
            self.rect.bottom = self.altura_tela
            self.velocidade_y *= -1
        if self.rect.left < self.largura_tela * 0.6:
            self.rect.left = int(self.largura_tela * 0.6)
            self.velocidade_x *= -1
        if self.rect.right > self.largura_tela:
            self.rect.right = self.largura_tela
            self.velocidade_x *= -1

    def atirar(self, grupos_de_sprites):
        agora = pygame.time.get_ticks()
        if agora - self.timers['radial'] > self.cadencias['radial']:
            self.timers['radial'] = agora
            num_tiros = 12 + self.nivel
            for i in range(num_tiros):
                angulo = (360 / num_tiros) * i
                tiro = TiroBoss(self.rect.centerx, self.rect.centery, angulo)
                grupos_de_sprites['todos'].add(tiro)
                grupos_de_sprites['tiros_inimigos'].add(tiro)
        if self.jogadores_vivos and agora - self.timers['teleguiado'] > self.cadencias['teleguiado']:
            self.timers['teleguiado'] = agora
            alvo = random.choice(self.jogadores_vivos)
            missil = TiroTeleguiado(self.rect.centerx, self.rect.centery, alvo, self.nivel)
            grupos_de_sprites['todos'].add(missil)
            grupos_de_sprites['tiros_inimigos'].add(missil)

class BossTriangulo(BossBase):
    def __init__(self, nivel, jogadores_vivos, largura_tela, altura_tela):
        super().__init__(nivel, jogadores_vivos, largura_tela, altura_tela)
        self.image = pygame.Surface((150, 130), pygame.SRCALPHA)
        pygame.draw.polygon(self.image, VERMELHO, [(0, 0), (0, 130), (150, 65)])
        self.rect = self.image.get_rect(midright=(self.largura_tela - 20, self.altura_tela / 2))
        self.alvo_y = self.rect.centery
        self.velocidade_dash = 15
        self.timers['mira_tripla'] = pygame.time.get_ticks()
        self.cadencias = {'mira_tripla': 1200 - nivel * 70}

    def movimento(self):
        if abs(self.rect.centery - self.alvo_y) < 5:
            if self.jogadores_vivos:
                self.alvo_y = random.choice(self.jogadores_vivos).rect.centery
        else:
            self.rect.centery += (self.alvo_y - self.rect.centery) / self.velocidade_dash
        
        if self.rect.top < 0: self.rect.top = 0
        if self.rect.bottom > self.altura_tela: self.rect.bottom = self.altura_tela

    def atirar(self, grupos_de_sprites):
        agora = pygame.time.get_ticks()
        if agora - self.timers['mira_tripla'] > self.cadencias['mira_tripla']:
            self.timers['mira_tripla'] = agora
            for angulo in [-15, 0, 15]:
                tiro = TiroJogador(self.rect.left, self.rect.centery, 15, LARANJA, 180 + angulo)
                grupos_de_sprites['todos'].add(tiro)
                grupos_de_sprites['tiros_inimigos'].add(tiro)