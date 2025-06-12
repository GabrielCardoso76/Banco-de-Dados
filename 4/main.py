import pygame
import sys
import random
from settings import *
from sprites import *
from ui import *

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.relogio = pygame.time.Clock()
        self.tela_cheia = True 
        self.reiniciar_tela()
        self.num_jogadores = 1

    def reiniciar_tela(self):
        display_info = pygame.display.Info()
        if self.tela_cheia:
            self.LARGURA_TELA = display_info.current_w
            self.ALTURA_TELA = display_info.current_h
            self.tela = pygame.display.set_mode((self.LARGURA_TELA, self.ALTURA_TELA), pygame.FULLSCREEN)
        else:
            self.LARGURA_TELA = LARGURA_JANELA
            self.ALTURA_TELA = ALTURA_JANELA
            self.tela = pygame.display.set_mode((self.LARGURA_TELA, self.ALTURA_TELA))
        pygame.display.set_caption(TITULO)
    
    def toggle_fullscreen(self):
        self.tela_cheia = not self.tela_cheia
        self.reiniciar_tela()

    def loop_principal(self):
        while True:
            resultado_menu = tela_menu(self)
            if resultado_menu == "TELA_MUDOU":
                continue
            
            self.num_jogadores = resultado_menu
            self.loop_jogo()

    def loop_jogo(self):
        estado_jogo = "JOGANDO"
        nivel_atual = 1
        
        controles_p1 = {'cima': pygame.K_w, 'baixo': pygame.K_s, 'esquerda': pygame.K_a, 'direita': pygame.K_d, 'tiro': pygame.K_v, 'cura': pygame.K_b, 'bomba': pygame.K_c}
        controles_p2 = {'cima': pygame.K_UP, 'baixo': pygame.K_DOWN, 'esquerda': pygame.K_LEFT, 'direita': pygame.K_RIGHT, 'tiro': pygame.K_l, 'cura': pygame.K_k, 'bomba': pygame.K_o}
        jogadores_config = [{'id': 1, 'cor': AZUL, 'controles': controles_p1}, {'id': 2, 'cor': AMARELO, 'controles': controles_p2}]
        jogadores_em_partida = [Nave(0, 0, p['cor'], p['controles'], p['id']) for i, p in enumerate(jogadores_config) if i < self.num_jogadores]
        chefes = [BossCirculo, BossQuadrado, BossTriangulo]

        grupos_de_sprites = {
            'todos': pygame.sprite.Group(), 'jogadores': pygame.sprite.Group(),
            'tiros_jogadores': pygame.sprite.Group(), 'inimigos': pygame.sprite.Group(),
            'tiros_inimigos': pygame.sprite.Group(), 'boss': pygame.sprite.Group(),
            'bombas': pygame.sprite.Group(), 'explosoes': pygame.sprite.Group()
        }

        inimigos_derrotados = 0
        estado_fase = "INIMIGOS"

        def preparar_fase(nivel, jogadores_atuais):
            nonlocal inimigos_derrotados, estado_fase
            inimigos_derrotados = 0
            estado_fase = "INIMIGOS"
            inimigos_para_derrotar = 10 + (nivel - 1) * 2
            
            for grupo in grupos_de_sprites.values():
                for sprite in grupo:
                    if not isinstance(sprite, Nave): sprite.kill()
            
            for i, jogador in enumerate(jogadores_atuais):
                jogador.rect.center = (100, self.ALTURA_TELA / 2 + ((i * 100) - 50 if len(jogadores_atuais) > 1 else 0))
                jogador.vida = jogador.vida_maxima
                grupos_de_sprites['todos'].add(jogador)
                grupos_de_sprites['jogadores'].add(jogador)
            return inimigos_para_derrotar

        inimigos_para_derrotar = preparar_fase(nivel_atual, jogadores_em_partida)
        ultimo_spawn_inimigo = pygame.time.get_ticks()
        
        rodando = True
        while rodando:
            dt = self.relogio.tick(FPS) / 1000.0
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        acao = tela_pausa(self)
                        if acao == "REINICIAR": self.loop_jogo(); return
                        if acao == "MENU": return
                    for jogador in grupos_de_sprites['jogadores']:
                        if event.key == jogador.controles['cura']: jogador.usar_cura()
                        if event.key == jogador.controles['bomba']: jogador.usar_bomba(grupos_de_sprites)

            if not grupos_de_sprites['jogadores']:
                tela_se_fudeu(self, nivel_atual)
                return

            if estado_jogo == "JOGANDO":
                for inimigo in list(grupos_de_sprites['inimigos']):
                    if inimigo.rect.right < 0:
                        for jogador in grupos_de_sprites['jogadores']: jogador.receber_dano(DANO_INIMIGO_VAZADO)
                        inimigo.kill()

                if estado_fase == "INIMIGOS":
                    if pygame.time.get_ticks() - ultimo_spawn_inimigo > 2000 and len(grupos_de_sprites['inimigos']) < 8:
                        ultimo_spawn_inimigo = pygame.time.get_ticks()
                        tipos_inimigos = [Inimigo, Inimigo, Inimigo, InimigoZigZag, InimigoAtiradorMulti]
                        inimigo_escolhido = random.choice(tipos_inimigos)(self.LARGURA_TELA, self.ALTURA_TELA)
                        grupos_de_sprites['todos'].add(inimigo_escolhido)
                        grupos_de_sprites['inimigos'].add(inimigo_escolhido)
                    if inimigos_derrotados >= inimigos_para_derrotar:
                        estado_fase = "BOSS"
                        for inimigo in grupos_de_sprites['inimigos']: inimigo.kill()
                        boss_classe = chefes[(nivel_atual - 1) % len(chefes)]
                        boss = boss_classe(nivel_atual, list(grupos_de_sprites['jogadores']), self.LARGURA_TELA, self.ALTURA_TELA)
                        grupos_de_sprites['todos'].add(boss)
                        grupos_de_sprites['boss'].add(boss)
                
                grupos_de_sprites['todos'].update(dt, self, grupos_de_sprites)

                acertos_inimigos = pygame.sprite.groupcollide(grupos_de_sprites['inimigos'], grupos_de_sprites['tiros_jogadores'], False, True)
                for inimigo, tiros in acertos_inimigos.items():
                    inimigo.vida -= tiros[0].dano
                    if inimigo.vida <= 0:
                        inimigo.kill(); inimigos_derrotados += 1
                        for j in grupos_de_sprites['jogadores']: j.dinheiro += 10
                
                acertos_boss = pygame.sprite.groupcollide(grupos_de_sprites['boss'], grupos_de_sprites['tiros_jogadores'], False, True)
                for boss, tiros in acertos_boss.items():
                    boss.vida -= tiros[0].dano
                    if boss.vida <= 0:
                        boss.kill(); nivel_atual += 1
                        for j in grupos_de_sprites['jogadores']: j.dinheiro += 300
                        estado_jogo = "UPGRADE"
                
                acertos_jogadores = pygame.sprite.groupcollide(grupos_de_sprites['jogadores'], grupos_de_sprites['tiros_inimigos'], False, True)
                for jogador, tiros in acertos_jogadores.items(): jogador.receber_dano(tiros[0].dano)

                colisoes_corpo = pygame.sprite.groupcollide(grupos_de_sprites['jogadores'], grupos_de_sprites['inimigos'], False, True)
                for jogador, inimigos_colididos in colisoes_corpo.items():
                    jogador.receber_dano(DANO_COLISAO * len(inimigos_colididos)); inimigos_derrotados += len(inimigos_colididos)
                    for j in grupos_de_sprites['jogadores']: j.dinheiro += 10 * len(inimigos_colididos)
                
                colisoes_bomba = pygame.sprite.groupcollide(grupos_de_sprites['inimigos'], grupos_de_sprites['bombas'], True, True)
                for inimigo, bombas in colisoes_bomba.items():
                    explosao = Explosao(bombas[0].rect.center)
                    grupos_de_sprites['todos'].add(explosao); grupos_de_sprites['explosoes'].add(explosao); inimigos_derrotados += 1
                
                for explosao in grupos_de_sprites['explosoes']:
                    acertos = pygame.sprite.spritecollide(explosao, grupos_de_sprites['inimigos'], True)
                    if acertos:
                        inimigos_derrotados += len(acertos)
                        for j in grupos_de_sprites['jogadores']: j.dinheiro += 5 * len(acertos)

            elif estado_jogo == "UPGRADE":
                jogadores_vivos = list(grupos_de_sprites['jogadores'])
                jogadores_mortos = [p for p in jogadores_em_partida if p not in jogadores_vivos]
                tela_upgrade(self, jogadores_vivos, jogadores_mortos, self.num_jogadores)
                jogadores_em_partida = sorted(jogadores_vivos + jogadores_mortos, key=lambda j: j.numero_jogador)
                inimigos_para_derrotar = preparar_fase(nivel_atual, jogadores_em_partida)
                estado_jogo = "JOGANDO"

            self.tela.fill(PRETO)
            grupos_de_sprites['todos'].draw(self.tela)
            fonte_hud = pygame.font.Font(None, 40)
            desenhar_texto(f"Fase: {nivel_atual}", fonte_hud, BRANCO, self.tela, self.LARGURA_TELA / 2, 20, center=True)
            y_offset = 0
            for jogador in sorted(list(grupos_de_sprites['jogadores']), key=lambda j: j.numero_jogador):
                y_base = 20 + y_offset
                desenhar_texto(f"P{jogador.numero_jogador}", fonte_hud, jogador.cor, self.tela, 20, y_base)
                desenhar_barra_vida(self.tela, 120, y_base, jogador.vida, jogador.vida_maxima, jogador.cor, 200, 15)
                desenhar_texto(f"{int(jogador.vida)}/{jogador.vida_maxima}", pygame.font.Font(None, 22), BRANCO, self.tela, 122, y_base)
                desenhar_barra_calor(self.tela, 120, y_base + 20, jogador.calor_atual, jogador.calor_maximo, 200, 10, jogador.superaquecido)
                desenhar_texto(f"$:{jogador.dinheiro}", fonte_hud, AMARELO, self.tela, 20, y_base + 35)
                desenhar_texto(f"Curas[{pygame.key.name(jogador.controles['cura'])}]: {jogador.curas_disponiveis}", pygame.font.Font(None, 24), CIANO, self.tela, 20, y_base + 65)
                desenhar_texto(f"Bombas[{pygame.key.name(jogador.controles['bomba'])}]: {jogador.bombas_disponiveis}", pygame.font.Font(None, 24), LARANJA, self.tela, 170, y_base + 65)
                y_offset += 100
            
            if estado_fase == "BOSS" and grupos_de_sprites['boss']:
                boss = grupos_de_sprites['boss'].sprites()[0]
                desenhar_barra_vida(self.tela, self.LARGURA_TELA / 2 - 200, 50, boss.vida, boss.vida_maxima, VERMELHO, 400, 25)
                
            pygame.display.flip()

if __name__ == "__main__":
    jogo = Game()
    jogo.loop_principal()