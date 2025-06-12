import pygame
import random
import math
from settings import *

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
        self.bombas_teleguiadas_disponiveis = 0
        self.velocidade_base = 7
        self.dano_tiro_base = 15
        self.cadencia_tiro_base = 200
        self.nivel_velocidade = 0; self.nivel_dano = 0; self.nivel_cadencia = 0
        self.nivel_tipo_tiro = 0; self.nivel_resfriamento = 0
        self.velocidade = self.velocidade_base
        self.dano_tiro = self.dano_tiro_base
        self.cadencia_tiro = self.cadencia_tiro_base
        self.calor_atual = 0; self.calor_maximo = 100
        self.taxa_aumento_calor_base = 8; self.taxa_resfriamento_base = 12
        self.taxa_aumento_calor = self.taxa_aumento_calor_base
        self.taxa_resfriamento = self.taxa_resfriamento_base
        self.superaquecido = False; self.tempo_superaquecimento = 0; self.duracao_cooldown = 3000
        self.arma_ativa = 'normal'
        self.possui_tiro_triplo = False
        self.possui_laser = False
        self.possui_hexagono = False
        self.hexagono_ativo = False
        self.hexagono = None
        self.laser_ativo = None

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
        self.gerenciar_armas(teclas, dt, game, grupos_de_sprites)
        self.gerenciar_hexagono(grupos_de_sprites)

    def gerenciar_armas(self, teclas, dt, game, grupos_de_sprites):
        if self.arma_ativa != 'laser' and self.laser_ativo:
            self.laser_ativo.kill()
            self.laser_ativo = None

        if self.arma_ativa == 'normal':
            if teclas[self.controles['tiro']]:
                self.atirar_normal(grupos_de_sprites)
        elif self.arma_ativa == 'laser':
            if teclas[self.controles['tiro']] and not self.superaquecido:
                if not self.laser_ativo:
                    self.laser_ativo = TiroLaser(self, game)
                    grupos_de_sprites['todos'].add(self.laser_ativo)
                    grupos_de_sprites['tiros_jogadores'].add(self.laser_ativo)
                self.calor_atual += self.taxa_aumento_calor_base * 5 * dt
                if self.calor_atual >= self.calor_maximo:
                    self.calor_atual = self.calor_maximo
                    self.superaquecido = True
                    self.tempo_superaquecimento = pygame.time.get_ticks()
            else:
                if self.laser_ativo:
                    self.laser_ativo.kill()
                    self.laser_ativo = None
        
        if not (self.arma_ativa == 'laser' and teclas[self.controles['tiro']]):
            if self.calor_atual > 0:
                self.calor_atual -= self.taxa_resfriamento * dt
                if self.calor_atual < 0:
                    self.calor_atual = 0

        if self.superaquecido and (pygame.time.get_ticks() - self.tempo_superaquecimento > self.duracao_cooldown):
            self.superaquecido = False
            self.calor_atual = 0

    def gerenciar_hexagono(self, grupos_de_sprites):
        if self.hexagono_ativo and self.hexagono is None:
            self.hexagono = HexagonoDefensivo(self)
            grupos_de_sprites['todos'].add(self.hexagono)
            grupos_de_sprites['escutos'].add(self.hexagono)
        elif not self.hexagono_ativo and self.hexagono is not None:
            self.hexagono.kill()
            self.hexagono = None
    
    def atirar_normal(self, grupos_de_sprites):
        if self.superaquecido: return
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_tiro > self.cadencia_tiro:
            self.ultimo_tiro = agora
            if self.possui_tiro_triplo:
                for angulo in [-15, 0, 15]:
                    tiro = TiroJogador(self.rect.right, self.rect.centery, self.dano_tiro, self.cor, angulo)
                    grupos_de_sprites['todos'].add(tiro)
                    grupos_de_sprites['tiros_jogadores'].add(tiro)
            else:
                tiro = TiroJogador(self.rect.right, self.rect.centery, self.dano_tiro, self.cor)
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

    def usar_bomba(self, grupos_de_sprites, teleguiada=False):
        if teleguiada:
            if self.bombas_teleguiadas_disponiveis > 0:
                alvo = self.encontrar_alvo_proximo(grupos_de_sprites)
                if alvo:
                    bomba = BombaTeleguiada(self.rect.center, alvo)
                    grupos_de_sprites['todos'].add(bomba)
                    grupos_de_sprites['bombas'].add(bomba)
                    self.bombas_teleguiadas_disponiveis -= 1
        else:
            if self.bombas_disponiveis > 0:
                bomba = Bomba(self.rect.right, self.rect.centery)
                grupos_de_sprites['todos'].add(bomba)
                grupos_de_sprites['bombas'].add(bomba)
                self.bombas_disponiveis -= 1
    
    def encontrar_alvo_proximo(self, grupos_de_sprites):
        alvos_potenciais = grupos_de_sprites['inimigos'].sprites() + grupos_de_sprites['boss'].sprites()
        if not alvos_potenciais: return None
        alvo_proximo = min(alvos_potenciais, key=lambda alvo: math.hypot(self.rect.centerx - alvo.rect.centerx, self.rect.centery - alvo.rect.centery))
        return alvo_proximo

    def receber_dano(self, dano):
        self.vida -= dano
        if self.vida <= 0:
            self.vida = 0
            self.kill()

    def reset_stats(self):
        self.nivel_velocidade = 0; self.nivel_dano = 0; self.nivel_cadencia = 0; self.nivel_tipo_tiro = 0; self.nivel_resfriamento = 0
        self.velocidade = self.velocidade_base; self.dano_tiro = self.dano_tiro_base; self.cadencia_tiro = self.cadencia_tiro_base
        self.taxa_aumento_calor = self.taxa_aumento_calor_base; self.taxa_resfriamento = self.taxa_resfriamento_base
        self.arma_ativa = 'normal'; self.possui_tiro_triplo = False; self.possui_laser = False; self.possui_hexagono = False; self.hexagono_ativo = False
        if self.hexagono: self.hexagono.kill(); self.hexagono = None
        if self.laser_ativo: self.laser_ativo.kill(); self.laser_ativo = None

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

class TiroLaser(pygame.sprite.Sprite):
    def __init__(self, jogador, game):
        super().__init__()
        self.jogador = jogador
        self.image = pygame.Surface((game.LARGURA_TELA, 5), pygame.SRCALPHA)
        self.image.fill(jogador.cor)
        self.rect = self.image.get_rect(midleft=self.jogador.rect.midright)
        self.dano = 0.5 

    def update(self, dt, game, grupos_de_sprites):
        if not self.jogador.alive():
            self.kill()
            return
        self.rect.midleft = self.jogador.rect.midright
        
        acertos_inimigos = pygame.sprite.spritecollide(self, grupos_de_sprites['inimigos'], False)
        for inimigo in acertos_inimigos:
            inimigo.vida -= self.dano
        
        acertos_boss = pygame.sprite.spritecollide(self, grupos_de_sprites['boss'], False)
        for boss in acertos_boss:
            boss.vida -= self.dano * 2

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
        if distancia == 0: return
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

class BombaTeleguiada(Bomba):
    def __init__(self, pos_inicial, alvo):
        super().__init__(pos_inicial[0], pos_inicial[1])
        self.alvo = alvo
        self.velocidade = 3
    def update(self, dt, game, grupos_de_sprites):
        if not self.alvo.alive():
            self.velocidade_x = 4
            self.rect.x += self.velocidade_x
        else:
            dx = self.alvo.rect.centerx - self.rect.centerx
            dy = self.alvo.rect.centery - self.rect.centery
            distancia = math.hypot(dx, dy)
            if distancia == 0: return
            dx, dy = dx / distancia, dy / distancia
            self.rect.x += dx * self.velocidade
            self.rect.y += dy * self.velocidade
        if not game.tela.get_rect().colliderect(self.rect):
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

class HexagonoDefensivo(pygame.sprite.Sprite):
    def __init__(self, jogador):
        super().__init__()
        self.jogador = jogador
        self.image_original = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.polygon(self.image_original, CIANO, [(15, 0), (30, 8), (30, 22), (15, 30), (0, 22), (0, 8)], 3)
        self.image = self.image_original
        self.rect = self.image.get_rect()
        self.angulo = 0
        self.raio_orbita = 60
        self.dano = 10
    def update(self, dt, game, grupos_de_sprites):
        if not self.jogador.alive():
            self.kill()
            return
        self.angulo += 4 * dt
        self.rect.centerx = self.jogador.rect.centerx + math.cos(self.angulo) * self.raio_orbita
        self.rect.centery = self.jogador.rect.centery + math.sin(self.angulo) * self.raio_orbita

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
            self.kill()
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

class Shuriken(TiroTeleguiado):
    def __init__(self, x, y, alvo, nivel):
        super().__init__(x, y, alvo, nivel)
        self.image_original = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.polygon(self.image_original, CINZA_ESCURO, [(10,0), (20,10), (10,20), (0,10)], 3)
        self.image = self.image_original
        self.dano = 10
        self.vida = 1
        self.angulo_rotacao = 0
    def update(self, dt, game, grupos_de_sprites):
        super().update(dt, game, grupos_de_sprites)
        self.angulo_rotacao += 10
        self.image = pygame.transform.rotate(self.image_original, self.angulo_rotacao)
        self.rect = self.image.get_rect(center=self.rect.center)
        if pygame.sprite.spritecollide(self, grupos_de_sprites['tiros_jogadores'], True):
            self.kill()

class BossBase(pygame.sprite.Sprite):
    def __init__(self, nivel, jogadores_vivos, game):
        super().__init__()
        self.jogadores_vivos = jogadores_vivos
        self.nivel = nivel
        self.game = game
        self.dificuldade = 1 + (nivel - 1) * 0.25
        self.vida = (1000 + nivel * 300) * self.dificuldade
        self.vida_maxima = self.vida
        self.timers = {'aliado': pygame.time.get_ticks()}
    def update(self, dt, game, grupos_de_sprites):
        self.movimento()
        self.atirar(grupos_de_sprites)
        self.invocar_aliados(grupos_de_sprites)
    def movimento(self): pass
    def atirar(self, grupos_de_sprites): pass
    def invocar_aliados(self, grupos_de_sprites):
        agora = pygame.time.get_ticks()
        vida_ratio = self.vida / self.vida_maxima
        cadencia_aliado = 1500 + (vida_ratio * 4000)
        if agora - self.timers['aliado'] > cadencia_aliado:
            self.timers['aliado'] = agora
            inimigo = InimigoZigZag(self.game.LARGURA_TELA, self.game.ALTURA_TELA)
            grupos_de_sprites['todos'].add(inimigo)
            grupos_de_sprites['inimigos'].add(inimigo)

class BossQuadrado(BossBase):
    def __init__(self, nivel, jogadores_vivos, game):
        super().__init__(nivel, jogadores_vivos, game)
        self.image = pygame.Surface((120, 120)); self.image.fill(VERMELHO)
        self.rect = self.image.get_rect(midright=(self.game.LARGURA_TELA - 20, self.game.ALTURA_TELA / 2))
        self.velocidade_y_base = (4 + nivel * 0.5) * self.dificuldade
        self.velocidade_y = self.velocidade_y_base
        self.timers.update({'tiro_parede': 0, 'super_ataque': 0, 'cura': pygame.time.get_ticks()})
        self.cadencias = {'tiro_parede': 2500 - nivel * 100, 'super_ataque': 15000}
        self.super_ativo = False
        self.tempo_fim_super = 0

    def movimento(self):
        self.rect.y += self.velocidade_y
        if self.rect.top < 0: self.rect.top = 0; self.velocidade_y *= -1
        if self.rect.bottom > self.game.ALTURA_TELA: self.rect.bottom = self.game.ALTURA_TELA; self.velocidade_y *= -1
    
    def update(self, dt, game, grupos_de_sprites):
        super().update(dt, game, grupos_de_sprites)
        agora = pygame.time.get_ticks()
        if agora - self.timers['cura'] > 80000:
            self.timers['cura'] = agora
            self.vida += self.vida_maxima * 0.07
            if self.vida > self.vida_maxima: self.vida = self.vida_maxima
        if self.super_ativo and agora > self.tempo_fim_super:
            self.super_ativo = False
            self.velocidade_y = self.velocidade_y_base

    def atirar(self, grupos_de_sprites):
        agora = pygame.time.get_ticks()
        if agora - self.timers['super_ataque'] > self.cadencias['super_ataque'] and not self.super_ativo:
            self.timers['super_ataque'] = agora
            self.super_ativo = True
            self.velocidade_y = self.velocidade_y_base * 1.5
            self.tempo_fim_super = agora + 5000
        
        if self.super_ativo:
            if agora % 200 < 50:
                for angulo in range(0, 360, 45):
                    tiro = TiroBoss(self.rect.centerx, self.rect.centery, angulo)
                    grupos_de_sprites['todos'].add(tiro)
                    grupos_de_sprites['tiros_inimigos'].add(tiro)
        elif agora - self.timers['tiro_parede'] > self.cadencias['tiro_parede']:
            self.timers['tiro_parede'] = agora
            for i in range(10):
                tiro = TiroInimigo(self.rect.left, self.rect.top + i * 12)
                grupos_de_sprites['todos'].add(tiro)
                grupos_de_sprites['tiros_inimigos'].add(tiro)

class BossCirculo(BossBase):
    def __init__(self, nivel, jogadores_vivos, game):
        super().__init__(nivel, jogadores_vivos, game)
        self.image = pygame.Surface((130, 130), pygame.SRCALPHA); pygame.draw.circle(self.image, VERMELHO, (65, 65), 65)
        self.rect = self.image.get_rect(midright=(self.game.LARGURA_TELA - 20, self.game.ALTURA_TELA / 2))
        self.velocidade_x = (1 + nivel * 0.2) * self.dificuldade
        self.velocidade_y = (2 + nivel * 0.5) * self.dificuldade
        self.timers.update({'radial': 0, 'teleguiado': 0, 'super_radial': pygame.time.get_ticks()})
        self.cadencias = {'radial': 2000 - nivel * 150, 'teleguiado': 7000 - nivel * 300, 'super_radial': 20000}
    def movimento(self):
        self.rect.y += self.velocidade_y; self.rect.x -= self.velocidade_x
        if self.rect.top < 0: self.rect.top = 0; self.velocidade_y *= -1
        if self.rect.bottom > self.game.ALTURA_TELA: self.rect.bottom = self.game.ALTURA_TELA; self.velocidade_y *= -1
        if self.rect.left < self.game.LARGURA_TELA * 0.6: self.rect.left = int(self.game.LARGURA_TELA * 0.6); self.velocidade_x *= -1
        if self.rect.right > self.game.LARGURA_TELA: self.rect.right = self.game.LARGURA_TELA; self.velocidade_x *= -1
    def atirar(self, grupos_de_sprites):
        agora = pygame.time.get_ticks()
        if agora - self.timers['super_radial'] > self.cadencias['super_radial']:
            self.timers['super_radial'] = agora; num_tiros = 40 + self.nivel * 4
            for i in range(num_tiros):
                angulo = (360 / num_tiros) * i
                tiro = TiroBoss(self.rect.centerx, self.rect.centery, angulo); grupos_de_sprites['todos'].add(tiro); grupos_de_sprites['tiros_inimigos'].add(tiro)
        if agora - self.timers['radial'] > self.cadencias['radial']:
            self.timers['radial'] = agora; num_tiros = 12 + self.nivel
            for i in range(num_tiros):
                angulo = (360 / num_tiros) * i
                tiro = TiroBoss(self.rect.centerx, self.rect.centery, angulo); grupos_de_sprites['todos'].add(tiro); grupos_de_sprites['tiros_inimigos'].add(tiro)
        if self.jogadores_vivos and agora - self.timers['teleguiado'] > self.cadencias['teleguiado']:
            self.timers['teleguiado'] = agora; alvo = random.choice(self.jogadores_vivos)
            missil = TiroTeleguiado(self.rect.centerx, self.rect.centery, alvo, self.nivel); grupos_de_sprites['todos'].add(missil); grupos_de_sprites['tiros_inimigos'].add(missil)

class BossTriangulo(BossBase):
    def __init__(self, nivel, jogadores_vivos, game):
        super().__init__(nivel, jogadores_vivos, game)
        self.image = pygame.Surface((150, 130), pygame.SRCALPHA); pygame.draw.polygon(self.image, VERMELHO, [(0, 0), (0, 130), (150, 65)])
        self.rect = self.image.get_rect(midright=(self.game.LARGURA_TELA - 20, self.game.ALTURA_TELA / 2))
        self.alvo_pos = pygame.math.Vector2(self.rect.center)
        self.velocidade_dash = (15 + self.dificuldade)
        self.timers['mira_tripla'] = 0; self.timers['super_shuriken'] = pygame.time.get_ticks()
        self.cadencias = {'mira_tripla': 1200 - nivel * 70, 'super_shuriken': 18000}
    def movimento(self):
        pos_atual = pygame.math.Vector2(self.rect.center)
        if pos_atual.distance_to(self.alvo_pos) < self.velocidade_dash:
            if self.jogadores_vivos:
                alvo_jogador = random.choice(self.jogadores_vivos)
                self.alvo_pos = pygame.math.Vector2(random.uniform(self.game.LARGURA_TELA * 0.7, self.game.LARGURA_TELA - 50), alvo_jogador.rect.centery)
        else:
            direcao = (self.alvo_pos - pos_atual).normalize()
            pos_atual += direcao * self.velocidade_dash
            self.rect.center = pos_atual
        if self.rect.top < 0: self.rect.top = 0
        if self.rect.bottom > self.game.ALTURA_TELA: self.rect.bottom = self.game.ALTURA_TELA
    def atirar(self, grupos_de_sprites):
        agora = pygame.time.get_ticks()
        if agora - self.timers['super_shuriken'] > self.cadencias['super_shuriken']:
            self.timers['super_shuriken'] = agora
            if self.jogadores_vivos:
                for alvo in self.jogadores_vivos:
                    shuriken = Shuriken(self.rect.centerx, self.rect.centery, alvo, self.nivel)
                    grupos_de_sprites['todos'].add(shuriken)
                    grupos_de_sprites['tiros_inimigos'].add(shuriken)
        if agora - self.timers['mira_tripla'] > self.cadencias['mira_tripla']:
            self.timers['mira_tripla'] = agora
            for angulo in [-15, 0, 15]:
                tiro = TiroJogador(self.rect.left, self.rect.centery, 15, LARANJA, 180 + angulo)
                grupos_de_sprites['todos'].add(tiro)
                grupos_de_sprites['tiros_inimigos'].add(tiro)