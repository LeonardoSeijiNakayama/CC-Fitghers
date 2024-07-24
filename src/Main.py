import pygame
from Player1 import Player1

pygame.init()

# Criando a janela de jogo
LARGURA_TELA = 1000
ALTURA_TELA = 600

VERDE = (0, 255, 0)
VERMELHO = (255, 0, 0)
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)

# Definindo variáveis

TAMANHO_THAUAN = 270
ESCALA_THAUAN = 1.5
OFFSET_THAUAN = [112, 107]
INFO_THAUAN = [TAMANHO_THAUAN, ESCALA_THAUAN, OFFSET_THAUAN]

janela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("CC FIGHTERS")

# Seta frame rate
clock = pygame.time.Clock()
FPS = 60

# Carregando background
bg_imagem = pygame.image.load("res/backgrounds/Palomakoba.png").convert_alpha()

# Carrega spritesheets


thauan_sheet = pygame.image.load("res/personagens/thauan/SpritesheetThauan5.png").convert_alpha()

# Definindo número de sprites para animações
THAUAN_ANIMACAO_SPRITES = [4, 3, 1, 6, 6, 1, 4]

# Função para desenhar background
def desenha_bg():
    escala_bg = pygame.transform.scale(bg_imagem, (LARGURA_TELA, ALTURA_TELA))
    janela.blit(escala_bg, (0, 0))

# Desenha barra de vida
def desenha_hp(vida, x, y):
    ratio = vida / 100
    pygame.draw.rect(janela, BRANCO, (x - 2, y - 2, 404, 34))
    pygame.draw.rect(janela, VERMELHO, (x, y, 400, 30))
    pygame.draw.rect(janela, VERDE, (x, y, 400 * ratio, 30))

# Função para desenhar o menu principal
def desenha_menu():
    janela.fill(PRETO)
    fonte = pygame.font.SysFont("Arial", 60)
    texto = fonte.render("CC FIGHTERS", True, BRANCO)
    janela.blit(texto, (LARGURA_TELA // 2 - texto.get_width() // 2, 100))
    
    fonte_botao = pygame.font.SysFont("Arial", 40)
    botao_play = pygame.Rect(LARGURA_TELA // 2 - 100, 300, 200, 80)
    pygame.draw.rect(janela, VERMELHO, botao_play)
    texto_play = fonte_botao.render("PLAY", True, BRANCO)
    janela.blit(texto_play, (LARGURA_TELA // 2 - texto_play.get_width() // 2, 315))
    
    return botao_play

# Função para desenhar a mensagem de vitória
def desenha_vitoria(vencedor):
    fonte = pygame.font.SysFont("Arial", 60)
    texto = fonte.render(f"Player {vencedor} Venceu!", True, PRETO)
    janela.blit(texto, (LARGURA_TELA // 2 - texto.get_width() // 2, ALTURA_TELA // 2 - texto.get_height() // 2))

# Criando dois lutadores
p1 = Player1(1, 200, 350, False, thauan_sheet, INFO_THAUAN, THAUAN_ANIMACAO_SPRITES)
p2 = Player1(2, 700, 350, True, thauan_sheet, INFO_THAUAN, THAUAN_ANIMACAO_SPRITES)

# Variáveis de controle
menu_principal = True
jogo_ativo = False
vencedor = None
tempo_vitoria = 0
TEMPO_ESPERA = 3000  # 3 segundos de espera

# Loop do jogo
run = True
while run:
    clock.tick(FPS)
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            run = False
    
    if menu_principal:
        botao_play = desenha_menu()
        
        for evento in pygame.event.get():
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if botao_play.collidepoint(evento.pos):
                    menu_principal = False
                    jogo_ativo = True
        
        pygame.display.update()
    
    else:
        # Desenhando background
        desenha_bg()
        
        # Desenha barra de vida
        desenha_hp(p1.vida, 20, 20)
        desenha_hp(p2.vida, 580, 20)
        
        # Movimenta jogadores
        p1.move(LARGURA_TELA, ALTURA_TELA, janela, p2)
        p2.move(LARGURA_TELA, ALTURA_TELA, janela, p1)
        
        # Atualiza animação
        p1.update()
        p2.update()
        
        # Desenhando players
        p1.draw(janela)
        p2.draw(janela)
        
        # Verifica se algum jogador morreu
        if not p1.vivo or not p2.vivo:
            if vencedor is None:
                vencedor = 1 if p2.vida <= 0 else 2
                tempo_vitoria = pygame.time.get_ticks()
        
        if vencedor is not None:
            desenha_vitoria(vencedor)
            if pygame.time.get_ticks() - tempo_vitoria > TEMPO_ESPERA:
                menu_principal = True
                jogo_ativo = False
                p1 = Player1(1, 200, 350, False, thauan_sheet, INFO_THAUAN, THAUAN_ANIMACAO_SPRITES)
                p2 = Player1(2, 700, 350, True, thauan_sheet, INFO_THAUAN, THAUAN_ANIMACAO_SPRITES)
                vencedor = None
        
        pygame.display.update()

# Fechando pygame
pygame.quit()
