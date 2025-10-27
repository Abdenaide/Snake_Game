import pygame
import random
import os

# Inicializa pygame
pygame.init()

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (200, 0, 0)
VERDE = (0, 200, 0)
AZUL = (50, 153, 213)
AMARELO = (255, 255, 0)

# Tela
LARGURA = 600
ALTURA = 400
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("🐍 Jogo da Cobrinha Avançado")

# Configurações
TAMANHO_COBRA = 10
FPS = 15
fonte = pygame.font.SysFont("bahnschrift", 25)

# Ranking
ARQUIVO_RANKING = "ranking.txt"

def carregar_ranking():
    if os.path.exists(ARQUIVO_RANKING):
        with open(ARQUIVO_RANKING, "r") as f:
            return sorted([int(x.strip()) for x in f.readlines() if x.strip().isdigit()], reverse=True)
    return []

def salvar_ranking(pontos):
    ranking = carregar_ranking()
    ranking.append(pontos)
    ranking = sorted(ranking, reverse=True)[:5]  # mantém só top 5
    with open(ARQUIVO_RANKING, "w") as f:
        for r in ranking:
            f.write(str(r) + "\n")

def mostrar_texto(msg, cor, x, y, tamanho=25):
    fonte_usada = pygame.font.SysFont("bahnschrift", tamanho)
    texto = fonte_usada.render(msg, True, cor)
    TELA.blit(texto, [x, y])

def nossa_cobra(cobra_pixels):
    for pixel in cobra_pixels:
        pygame.draw.rect(TELA, VERDE, [pixel[0], pixel[1], TAMANHO_COBRA, TAMANHO_COBRA])

def jogo(velocidade):
    fim_jogo = False
    game_over = False

    x = LARGURA / 2
    y = ALTURA / 2
    x_mudanca = 0
    y_mudanca = 0

    cobra_pixels = []
    comprimento_cobra = 1

    comida_x = round(random.randrange(0, LARGURA - TAMANHO_COBRA) / 10.0) * 10.0
    comida_y = round(random.randrange(0, ALTURA - TAMANHO_COBRA) / 10.0) * 10.0

    clock = pygame.time.Clock()

    while not fim_jogo:
        while game_over:
            TELA.fill(PRETO)
            mostrar_texto("Você perdeu! Pressione C para jogar de novo ou Q para sair", VERMELHO, 50, ALTURA / 3, 20)
            pontos = comprimento_cobra - 1
            mostrar_texto(f"Pontos: {pontos}", BRANCO, 10, 10)
            salvar_ranking(pontos)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        fim_jogo = True
                        game_over = False
                    if event.key == pygame.K_c:
                        jogo(velocidade)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fim_jogo = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x_mudanca == 0:
                    x_mudanca = -TAMANHO_COBRA
                    y_mudanca = 0
                elif event.key == pygame.K_RIGHT and x_mudanca == 0:
                    x_mudanca = TAMANHO_COBRA
                    y_mudanca = 0
                elif event.key == pygame.K_UP and y_mudanca == 0:
                    y_mudanca = -TAMANHO_COBRA
                    x_mudanca = 0
                elif event.key == pygame.K_DOWN and y_mudanca == 0:
                    y_mudanca = TAMANHO_COBRA
                    x_mudanca = 0

        if x >= LARGURA or x < 0 or y >= ALTURA or y < 0:
            game_over = True

        x += x_mudanca
        y += y_mudanca
        TELA.fill(AZUL)
        pygame.draw.rect(TELA, VERMELHO, [comida_x, comida_y, TAMANHO_COBRA, TAMANHO_COBRA])
        cobra_pixels.append([x, y])

        if len(cobra_pixels) > comprimento_cobra:
            del cobra_pixels[0]

        for pixel in cobra_pixels[:-1]:
            if pixel == [x, y]:
                game_over = True

        nossa_cobra(cobra_pixels)
        mostrar_texto("Pontos: " + str(comprimento_cobra - 1), BRANCO, 10, 10)

        pygame.display.update()

        if x == comida_x and y == comida_y:
            comida_x = round(random.randrange(0, LARGURA - TAMANHO_COBRA) / 10.0) * 10.0
            comida_y = round(random.randrange(0, ALTURA - TAMANHO_COBRA) / 10.0) * 10.0
            comprimento_cobra += 1

        clock.tick(velocidade)

    pygame.quit()

def menu():
    em_menu = True
    while em_menu:
        TELA.fill(PRETO)
        mostrar_texto("🐍 JOGO DA COBRINHA 🐍", AMARELO, 150, 50, 30)
        mostrar_texto("1 - Jogar (Normal)", VERDE, 200, 150)
        mostrar_texto("2 - Jogar (Difícil)", VERDE, 200, 180)
        mostrar_texto("3 - Jogar (Insano)", VERDE, 200, 210)
        mostrar_texto("R - Ranking", AZUL, 200, 240)
        mostrar_texto("Q - Sair", VERMELHO, 200, 270)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                em_menu = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    jogo(15)   # Normal
                elif event.key == pygame.K_2:
                    jogo(25)   # Difícil
                elif event.key == pygame.K_3:
                    jogo(35)   # Insano
                elif event.key == pygame.K_r:
                    mostrar_ranking()
                elif event.key == pygame.K_q:
                    em_menu = False

def mostrar_ranking():
    ranking = carregar_ranking()
    mostrando = True
    while mostrando:
        TELA.fill(PRETO)
        mostrar_texto("🏆 RANKING 🏆", AMARELO, 220, 50, 30)
        if ranking:
            for i, score in enumerate(ranking):
                mostrar_texto(f"{i+1}º - {score} pontos", BRANCO, 200, 120 + i*30)
        else:
            mostrar_texto("Nenhum jogo registrado!", VERMELHO, 180, 200)

        mostrar_texto("Pressione ESC para voltar", AZUL, 180, 350)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mostrando = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                mostrando = False



menu()
