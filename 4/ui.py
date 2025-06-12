import pygame
import sys
from settings import *

# --- Classes de UI ---
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
        if not self.ativo:
            return
        mouse_pos = pygame.mouse.get_pos()
        cor_atual = self.cor_hover if self.rect.collidepoint(mouse_pos) else self.cor_fundo
        pygame.draw.rect(superficie, cor_atual, self.rect, border_radius=5)
        desenhar_texto(self.texto, self.fonte, self.cor_texto, superficie, self.rect.centerx, self.rect.centery, center=True)

    def foi_clicado(self, evento):
        if not self.ativo:
            return False
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            return self.rect.collidepoint(evento.pos)
        return False

# --- Funções de Desenho ---
def desenhar_texto(texto, fonte, cor, superficie, x, y, center=False):
    textobj = fonte.render(texto, True, cor)
    textrect = textobj.get_rect()
    if center:
        textrect.center = (x, y)
    else:
        textrect.topleft = (x, y)
    superficie.blit(textobj, textrect)

def desenhar_barra_vida(superficie, x, y, vida_atual, vida_maxima, cor, largura, altura):
    if vida_atual < 0:
        vida_atual = 0
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

# --- Telas de Jogo ---
def tela_menu(game):
    fonte_titulo = pygame.font.Font(None, 100)
    fonte_opcao = pygame.font.Font(None, 60)
    
    largura, altura = game.LARGURA_TELA, game.ALTURA_TELA
    
    while True:
        game.tela.fill(PRETO)
        desenhar_texto("ALEXANDRE, O REI", fonte_titulo, BRANCO, game.tela, largura / 2, altura / 4, center=True)
        
        mouse_x, mouse_y = pygame.mouse.get_pos()

        botao_1p = pygame.Rect(largura / 2 - 150, altura / 2 - 70, 300, 60)
        botao_2p = pygame.Rect(largura / 2 - 150, altura / 2 + 10, 300, 60)
        botao_tela = pygame.Rect(largura / 2 - 150, altura / 2 + 90, 300, 60)
        botao_sair = pygame.Rect(largura / 2 - 150, altura / 2 + 170, 300, 60)

        texto_tela = "Tela Cheia" if not game.tela_cheia else "Modo Janela"
        
        botoes = [(botao_1p, "1 Jogador"), (botao_2p, "2 Jogadores"), (botao_tela, texto_tela), (botao_sair, "Sair")]

        for botao, texto in botoes:
            if botao.collidepoint((mouse_x, mouse_y)):
                pygame.draw.rect(game.tela, AZUL, botao)
            else:
                pygame.draw.rect(game.tela, BRANCO, botao, 3)
            desenhar_texto(texto, fonte_opcao, BRANCO, game.tela, botao.centerx, botao.centery, center=True)

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if botao_1p.collidepoint((mouse_x, mouse_y)): return 1
                if botao_2p.collidepoint((mouse_x, mouse_y)): return 2
                if botao_tela.collidepoint((mouse_x, mouse_y)):
                    game.toggle_fullscreen()
                    return "TELA_MUDOU" 
                if botao_sair.collidepoint((mouse_x, mouse_y)):
                    pygame.quit()
                    sys.exit()
        pygame.display.update()

def tela_pausa(game):
    fonte_titulo = pygame.font.Font(None, 80)
    fonte_opcao = pygame.font.Font(None, 50)
    overlay = pygame.Surface((game.LARGURA_TELA, game.ALTURA_TELA), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))
    game.tela.blit(overlay, (0, 0))
    desenhar_texto("PAUSADO", fonte_titulo, BRANCO, game.tela, game.LARGURA_TELA / 2, game.ALTURA_TELA / 4, center=True)
    
    largura, altura = game.LARGURA_TELA, game.ALTURA_TELA
    botao_continuar = pygame.Rect(largura / 2 - 150, altura / 2 - 50, 300, 50)
    botao_reiniciar = pygame.Rect(largura / 2 - 150, altura / 2 + 20, 300, 50)
    botao_sair_menu = pygame.Rect(largura / 2 - 150, altura / 2 + 90, 300, 50)

    while True:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        
        for botao, texto in [(botao_continuar, "Continuar"), (botao_reiniciar, "Reiniciar Fase"), (botao_sair_menu, "Sair para o Menu")]:
            if botao.collidepoint((mouse_x, mouse_y)):
                pygame.draw.rect(game.tela, AZUL, botao)
            else:
                pygame.draw.rect(game.tela, BRANCO, botao, 2)
            desenhar_texto(texto, fonte_opcao, BRANCO, game.tela, botao.centerx, botao.centery, center=True)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: return "CONTINUAR"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if botao_continuar.collidepoint((mouse_x, mouse_y)): return "CONTINUAR"
                if botao_reiniciar.collidepoint((mouse_x, mouse_y)): return "REINICIAR"
                if botao_sair_menu.collidepoint((mouse_x, mouse_y)): return "MENU"
        pygame.display.update()

def tela_se_fudeu(game, nivel):
    fonte_titulo = pygame.font.Font(None, 150)
    fonte_sub = pygame.font.Font(None, 70)
    game.tela.fill(PRETO)
    desenhar_texto("SE FUDEU", fonte_titulo, VERMELHO, game.tela, game.LARGURA_TELA / 2, game.ALTURA_TELA / 3, center=True)
    desenhar_texto(f"Você morreu na Fase {nivel}", fonte_sub, BRANCO, game.tela, game.LARGURA_TELA / 2, game.ALTURA_TELA / 2, center=True)
    botao_menu = Botao(game.LARGURA_TELA / 2 - 150, game.ALTURA_TELA * 0.6, 300, 60, "Voltar ao Menu")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if botao_menu.foi_clicado(event): return
        botao_menu.desenhar(game.tela)
        pygame.display.update()

def tela_upgrade(game, jogadores_vivos, jogadores_mortos, num_jogadores):
    custos = {'velocidade': 50, 'dano': 75, 'cadencia': 100, 'reviver': 200, 'tipo_tiro': 500, 'resfriamento': 120, 'cura': 60, 'bomba': 80}
    fonte_titulo = pygame.font.Font(None, 60)
    fonte_normal = pygame.font.Font(None, 30)
    botoes_por_jogador = {}
    todos_os_jogadores = sorted(jogadores_vivos + jogadores_mortos, key=lambda j: j.numero_jogador)
    espaco_entre_jogadores = game.LARGURA_TELA / (len(todos_os_jogadores) + 1)
    y_botoes = 200
    for i, jogador in enumerate(todos_os_jogadores):
        x_base = espaco_entre_jogadores * (i + 1)
        botoes_por_jogador[jogador.numero_jogador] = {
            'velocidade': Botao(x_base - 100, y_botoes, 200, 40, f"Velocidade (+${custos['velocidade']})"),
            'dano': Botao(x_base - 100, y_botoes + 50, 200, 40, f"Dano (+${custos['dano']})"),
            'cadencia': Botao(x_base - 100, y_botoes + 100, 200, 40, f"Cadência (+${custos['cadencia']})"),
            'resfriamento': Botao(x_base - 100, y_botoes + 150, 200, 40, f"Resfriamento (+${custos['resfriamento']})"),
            'tipo_tiro': Botao(x_base - 100, y_botoes + 200, 200, 40, f"Tiro Triplo (${custos['tipo_tiro']})"),
            'cura': Botao(x_base - 100, y_botoes + 250, 200, 40, f"Comprar Cura (+${custos['cura']})"),
            'bomba': Botao(x_base - 100, y_botoes + 300, 200, 40, f"Comprar Bomba (+${custos['bomba']})"),
            'cor': Botao(x_base - 100, y_botoes + 350, 200, 40, "Mudar Cor")
        }
    botao_reviver = None
    if num_jogadores == 2 and jogadores_vivos and jogadores_mortos:
        jogador_vivo = jogadores_vivos[0]
        jogador_morto = jogadores_mortos[0]
        botao_reviver = Botao(game.LARGURA_TELA / 2 - 125, game.ALTURA_TELA - 200, 250, 50, f"Reviver P{jogador_morto.numero_jogador} (${custos['reviver']})")
    botao_continuar = Botao(game.LARGURA_TELA / 2 - 100, game.ALTURA_TELA - 100, 200, 50, "Próxima Fase")
    rodando_upgrade = True
    while rodando_upgrade:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if botao_continuar.foi_clicado(event): rodando_upgrade = False
            if botao_reviver and botao_reviver.foi_clicado(event):
                if jogador_vivo.dinheiro >= custos['reviver']:
                    jogador_vivo.dinheiro -= custos['reviver']; jogador_morto.reset_stats(); jogadores_vivos.append(jogador_morto); jogadores_mortos.remove(jogador_morto); botao_reviver.ativo = False
            for j in jogadores_vivos:
                botoes = botoes_por_jogador[j.numero_jogador]
                if botoes['velocidade'].foi_clicado(event) and j.dinheiro >= custos['velocidade']:
                    j.dinheiro -= custos['velocidade']; j.nivel_velocidade += 1; j.velocidade = j.velocidade_base + j.nivel_velocidade
                if botoes['dano'].foi_clicado(event) and j.dinheiro >= custos['dano']:
                    j.dinheiro -= custos['dano']; j.nivel_dano += 1; j.dano_tiro = j.dano_tiro_base + j.nivel_dano * 5
                if botoes['cadencia'].foi_clicado(event) and j.dinheiro >= custos['cadencia']:
                    j.dinheiro -= custos['cadencia']; j.nivel_cadencia += 1; j.cadencia_tiro = max(50, j.cadencia_tiro_base - j.nivel_cadencia * 15)
                if botoes['resfriamento'].foi_clicado(event) and j.dinheiro >= custos['resfriamento']:
                    j.dinheiro -= custos['resfriamento']; j.nivel_resfriamento += 1
                    j.taxa_resfriamento = j.taxa_resfriamento_base + j.nivel_resfriamento * 2.5
                    j.taxa_aumento_calor = max(2, j.taxa_aumento_calor_base - j.nivel_resfriamento * 0.5)
                if botoes['tipo_tiro'].foi_clicado(event) and j.dinheiro >= custos['tipo_tiro'] and j.nivel_tipo_tiro == 0:
                    j.dinheiro -= custos['tipo_tiro']; j.nivel_tipo_tiro = 1
                if botoes['cura'].foi_clicado(event) and j.dinheiro >= custos['cura']:
                    j.dinheiro -= custos['cura']; j.curas_disponiveis += 1
                if botoes['bomba'].foi_clicado(event) and j.dinheiro >= custos['bomba']:
                    j.dinheiro -= custos['bomba']; j.bombas_disponiveis += 1
                if botoes['cor'].foi_clicado(event):
                    j.cor_atual_index = (j.cor_atual_index + 1) % len(CORES_NAVE)
                    j.cor = CORES_NAVE[j.cor_atual_index]
                    j.atualizar_imagem()
        game.tela.fill(PRETO)
        desenhar_texto("LOJA DE UPGRADES", fonte_titulo, BRANCO, game.tela, game.LARGURA_TELA / 2, 50, center=True)
        for i, jogador in enumerate(todos_os_jogadores):
            x_base = espaco_entre_jogadores * (i + 1)
            status = "VIVO" if jogador in jogadores_vivos else "MORTO"
            cor_status = VERDE if status == "VIVO" else VERMELHO
            desenhar_texto(f"Jogador {jogador.numero_jogador}", fonte_titulo, jogador.cor, game.tela, x_base, 100, center=True)
            desenhar_texto(f"({status})", fonte_normal, cor_status, game.tela, x_base, 140, center=True)
            if status == "VIVO":
                desenhar_texto(f"Dinheiro: ${jogador.dinheiro}", fonte_normal, AMARELO, game.tela, x_base, 170, center=True)
                botoes = botoes_por_jogador[jogador.numero_jogador]
                if jogador.nivel_tipo_tiro >= 1: botoes['tipo_tiro'].ativo = False
                for b in botoes.values(): b.desenhar(game.tela)
                desenhar_texto(f"Nv. Vel: {jogador.nivel_velocidade} | Nv. Dano: {jogador.nivel_dano} | Nv. Cad: {jogador.nivel_cadencia}", fonte_normal, BRANCO, game.tela, x_base, y_botoes + 400, center=True)
                desenhar_texto(f"Nv. Resfr: {jogador.nivel_resfriamento} | Tiro: {'Triplo' if jogador.nivel_tipo_tiro > 0 else 'Único'}", fonte_normal, BRANCO, game.tela, x_base, y_botoes + 425, center=True)
        if botao_reviver: botao_reviver.desenhar(game.tela)
        botao_continuar.desenhar(game.tela)
        pygame.display.update()