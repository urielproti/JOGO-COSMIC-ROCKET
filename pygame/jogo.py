import pygame
import random
import sys

# === INICIALIZAÇÃO DO PYGAME ===
pygame.init()

# Música de fundo e som de colisão
pygame.mixer.init()
pygame.mixer.music.set_volume(0.15)
pygame.mixer.music.load("BoxCat Games - CPU Talk.mp3")  # música do jogo
pygame.mixer.music.play(-1)  # toca em loop

som_colisao = pygame.mixer.Sound("smw_kick.wav")  # som quando pega a estrela

# === CONFIGURAÇÕES DA JANELA ===
LARGURA, ALTURA = 600, 400
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("🚀 Rocket Cosmic - Uriel Proti")

# === CORES QUE VAMOS USAR ===
BRANCO   = (255, 255, 255)
AZUL     = (50, 50, 200)
AMARELO  = (255, 215, 0)
ROSA     = (255, 105, 180)
VERMELHO = (200, 0, 0)
LARANJA  = (255, 140, 0)

# Fonte para os textos
fonte = pygame.font.SysFont("arial", 28, bold=True)

# Controle de FPS
clock = pygame.time.Clock()
FPS = 10

# === FUNDO DO JOGO ===
fundo = pygame.image.load("espaco.png")
fundo = pygame.transform.scale(fundo, (LARGURA, ALTURA))

# === FUNÇÕES AUXILIARES ===
def desenhar_texto(texto, tamanho, cor, x, y, centralizado=True):
    """Desenha texto na tela em uma posição específica"""
    fonte = pygame.font.SysFont("arial", tamanho, bold=True)
    superficie = fonte.render(texto, True, cor)
    rect = superficie.get_rect()
    if centralizado:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    TELA.blit(superficie, rect)

def menu_inicial():
    """Tela inicial do jogo"""
    while True:
        TELA.blit(fundo, (0, 0))
        desenhar_texto("🚀 Rocket Cosmic 🌌", 40, AMARELO, LARGURA//2, ALTURA//4)
        desenhar_texto("Pressione ENTER para jogar", 28, BRANCO, LARGURA//2, ALTURA//2)
        desenhar_texto("Pressione ESC para sair", 24, VERMELHO, LARGURA//2, ALTURA//2 + 50)
        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:  # fecha a janela
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:  # tecla ENTER inicia
                    return
                if evento.key == pygame.K_ESCAPE:  # tecla ESC sai
                    pygame.quit()
                    sys.exit()

def game_over(pontos):
    """Tela de fim de jogo"""
    while True:
        TELA.blit(fundo, (0, 0))
        desenhar_texto("💥 Game Over 💥", 40, VERMELHO, LARGURA//2, ALTURA//4)
        desenhar_texto(f"Pontuação: {pontos}", 30, BRANCO, LARGURA//2, ALTURA//2)
        desenhar_texto("Pressione ENTER para jogar novamente", 24, BRANCO, LARGURA//2, ALTURA//2 + 60)
        desenhar_texto("Pressione ESC para sair", 24, VERMELHO, LARGURA//2, ALTURA//2 + 100)
        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:  # jogar de novo
                    return
                if evento.key == pygame.K_ESCAPE:  # sair
                    pygame.quit()
                    sys.exit()

def desenhar_foguete(x, y, direcao):
    """Desenha o foguete como um triângulo azul + chama animada"""
    # Corpo do foguete
    pygame.draw.polygon(TELA, AZUL, [(x, y), (x-10, y+20), (x+10, y+20)])
    # Chama de fogo (laranja + amarelo)
    pygame.draw.polygon(TELA, LARANJA, [(x, y+20), (x-5, y+30), (x+5, y+30)])
    pygame.draw.polygon(TELA, AMARELO, [(x, y+20), (x-2, y+27), (x+2, y+27)])

# === FUNÇÃO PRINCIPAL DO JOGO ===
def jogo():
    # Posição inicial do foguete
    foguete_pos = [LARGURA//2, ALTURA//2]
    direcao = "DIREITA"
    mudar_para = direcao

    # Posição inicial da estrela (pontos)
    star_pos = [random.randrange(1, (LARGURA//10)) * 10,
                random.randrange(1, (ALTURA//10)) * 10]
    star_spawn = True

    # Posição da maçã rosa (perigosa)
    apple_pos = [random.randrange(1, (LARGURA//10)) * 10,
                 random.randrange(1, (ALTURA//10)) * 10]

    pontos = 0  # contador de pontos

    # Loop principal do jogo
    while True:
        # --- CONTROLES DO JOGADOR ---
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP and direcao != "BAIXO":
                    mudar_para = "CIMA"
                elif evento.key == pygame.K_DOWN and direcao != "CIMA":
                    mudar_para = "BAIXO"
                elif evento.key == pygame.K_LEFT and direcao != "DIREITA":
                    mudar_para = "ESQUERDA"
                elif evento.key == pygame.K_RIGHT and direcao != "ESQUERDA":
                    mudar_para = "DIREITA"

        direcao = mudar_para

        # Movimento do foguete
        if direcao == "CIMA":
            foguete_pos[1] -= 10
        if direcao == "BAIXO":
            foguete_pos[1] += 10
        if direcao == "ESQUERDA":
            foguete_pos[0] -= 10
        if direcao == "DIREITA":
            foguete_pos[0] += 10

        # Retângulos para detectar colisão
        foguete_rect = pygame.Rect(foguete_pos[0]-10, foguete_pos[1], 20, 20)
        star_rect   = pygame.Rect(star_pos[0], star_pos[1], 10, 10)
        apple_rect  = pygame.Rect(apple_pos[0], apple_pos[1], 12, 12)

        # --- COLISÃO COM ESTRELA ---
        if foguete_rect.colliderect(star_rect):
            pontos += 10
            som_colisao.play()
            star_spawn = False

        if not star_spawn:  # reaparece em lugar aleatório
            star_pos = [random.randrange(1, (LARGURA//10)) * 10,
                        random.randrange(1, (ALTURA//10)) * 10]
            star_spawn = True

        # --- COLISÃO COM A MAÇÃ (game over) ---
        if foguete_rect.colliderect(apple_rect):
            game_over(pontos)
            return

        # --- DESENHO NA TELA ---
        TELA.blit(fundo, (0, 0))  # fundo do jogo
        desenhar_foguete(foguete_pos[0], foguete_pos[1], direcao)  # foguete
        pygame.draw.rect(TELA, AMARELO, star_rect)  # estrela
        pygame.draw.circle(TELA, ROSA, (apple_pos[0]+5, apple_pos[1]+5), 6)  # maçã
        desenhar_texto(f"Pontos: {pontos}", 24, BRANCO, 10, 10, centralizado=False)

        # --- COLISÃO COM AS BORDAS ---
        if foguete_pos[0] < 0 or foguete_pos[0] > LARGURA-10:
            game_over(pontos)
            return
        if foguete_pos[1] < 0 or foguete_pos[1] > ALTURA-10:
            game_over(pontos)
            return

        # Atualiza tela e controla FPS
        pygame.display.update()
        clock.tick(FPS)

# === LOOP PRINCIPAL DO JOGO ===
while True:
    menu_inicial()
    jogo()
