import sys
import pygame
import random
from pygame.locals import *

pygame.init()

# Screen dimensions
WIDTH = 640
HEIGHT = 480

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)

# Ball dimensions
BALL_SIZE = 20
BALL_SPEED = 5

# Paddle dimensions
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 60
PADDLE_SPEED = 5

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('2-Player 2-Ball Modified Pong')

# Inicializar pelotas y paletas
ball_1 = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2 - 50, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)
ball_2 = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2 + 50, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)
paddle_left = pygame.Rect(10, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
paddle_right = pygame.Rect(WIDTH - 20, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)

ball_1_dx = BALL_SPEED
ball_1_dy = 0
ball_2_dx = -BALL_SPEED
ball_2_dy = 0

paddle_left_dy = PADDLE_SPEED
paddle_right_dy = -PADDLE_SPEED

clock = pygame.time.Clock()

# Puntuación y vidas
score_1 = 0
score_2 = 0
lives_1 = 3
lives_2 = 3

# Fuente para mostrar la puntuación y las vidas
font_small = pygame.font.Font(None, 24)
font_large = pygame.font.Font(None, 48)
font_restart = pygame.font.Font(None, 20)

game_over = False
message = ""
show_restart_message = False

def draw_score_and_lives():
    for i in range(3):
        if i < lives_1:
            pygame.draw.circle(screen, WHITE, (20 + i * 30, 20), 10)
        else:
            pygame.draw.circle(screen, GRAY, (20 + i * 30, 20), 10)
        
        if i < lives_2:
            pygame.draw.circle(screen, WHITE, (WIDTH - 90 + i * 30, 20), 10)
        else:
            pygame.draw.circle(screen, GRAY, (WIDTH - 90 + i * 30, 20), 10)
    
    player1_text = font_small.render("Jugador 1", True, RED)
    player2_text = font_small.render("Jugador 2", True, BLUE)
    
    pygame.draw.line(screen, RED, (WIDTH // 2 - 100, 35), (WIDTH // 2 - 10, 35), 2)
    pygame.draw.line(screen, BLUE, (WIDTH // 2 + 10, 35), (WIDTH // 2 + 100, 35), 2)
    
    screen.blit(player1_text, (WIDTH // 2 - 100, 10))
    screen.blit(player2_text, (WIDTH // 2 + 10, 10))

def update_ball_positions():
    global ball_1, ball_2, ball_1_dx, ball_1_dy, ball_2_dx, ball_2_dy, lives_1, lives_2

    # Mover las pelotas
    ball_1.x += ball_1_dx
    ball_1.y += ball_1_dy
    ball_2.x += ball_2_dx
    ball_2.y += ball_2_dy

    # Comprobar colisiones con los bordes superior e inferior de la pantalla para ambas pelotas
    if ball_1.top <= 0:
        ball_1.top = 0  # Asegurarse de que no pase por encima
        ball_1_dy = -ball_1_dy
    elif ball_1.bottom >= HEIGHT:
        ball_1.bottom = HEIGHT  # Asegurarse de que no pase por debajo
        ball_1_dy = -ball_1_dy

    if ball_2.top <= 0:
        ball_2.top = 0  # Asegurarse de que no pase por encima
        ball_2_dy = -ball_2_dy
    elif ball_2.bottom >= HEIGHT:
        ball_2.bottom = HEIGHT  # Asegurarse de que no pase por debajo
        ball_2_dy = -ball_2_dy

    # Comprobar colisiones con los bordes laterales de la pantalla para la pelota 1
    if ball_1.left <= 0 or ball_1.right >= WIDTH:
        lives_1 -= 1
        reset_ball(1)
        print(f"Jugador 1 perdió una vida. Vidas restantes: {lives_1}")

    # Comprobar colisiones con los bordes laterales de la pantalla para la pelota 2
    if ball_2.left <= 0 or ball_2.right >= WIDTH:
        lives_2 -= 1
        reset_ball(2)
        print(f"Jugador 2 perdió una vida. Vidas restantes: {lives_2}")

def reset_ball(player):
    global ball_1, ball_2, ball_1_dx, ball_1_dy, ball_2_dx, ball_2_dy

    if player == 1:
        ball_1.x = WIDTH // 4
        ball_1.y = HEIGHT // 2
        ball_1_dx = random.choice([-BALL_SPEED, BALL_SPEED])
        ball_1_dy = random.choice([-BALL_SPEED, BALL_SPEED])
    else:
        ball_2.x = 3 * WIDTH // 4
        ball_2.y = HEIGHT // 2
        ball_2_dx = random.choice([-BALL_SPEED, BALL_SPEED])
        ball_2_dy = random.choice([-BALL_SPEED, BALL_SPEED])

def game_loop():
    global lives_1, lives_2

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        keys = pygame.key.get_pressed()
        move_balls(keys)
        update_ball_positions()  # Asegúrate de que esta línea esté presente
        update_speed()  # Llamar a la función para actualizar la velocidad

        screen.fill(BLACK)
        draw_paddles()
        draw_balls()
        draw_score_and_lives()

        if lives_1 <= 0 or lives_2 <= 0:
            game_over()
            return

        pygame.display.flip()
        clock.tick(60)

# Variables para controlar el tiempo y la velocidad
start_time = pygame.time.get_ticks()  # Tiempo de inicio
speed_increment_time = 1000  # 5 segundos en milisegundos
speed_multiplier = 1.0  # Multiplicador de velocidad

def update_speed():
    global ball_1_dx, ball_1_dy, ball_2_dx, ball_2_dy, paddle_left_dy, paddle_right_dy, speed_multiplier

    # Comprobar si han pasado 5 segundos
    current_time = pygame.time.get_ticks()
    if current_time - start_time >= speed_increment_time:
        speed_multiplier += 0.5  # Aumentar el multiplicador de velocidad
        ball_1_dx = BALL_SPEED * speed_multiplier
        ball_1_dy = BALL_SPEED * speed_multiplier
        ball_2_dx = -BALL_SPEED * speed_multiplier
        ball_2_dy = BALL_SPEED * speed_multiplier
        paddle_left_dy = PADDLE_SPEED * speed_multiplier
        paddle_right_dy = -PADDLE_SPEED * speed_multiplier
        # Reiniciar el tiempo de inicio
        start_time = current_time

while True:
    if game_over:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_RETURN:
                score_1 = 0
                score_2 = 0
                lives_1 = 3
                lives_2 = 3
                ball_1.x = WIDTH // 2 - BALL_SIZE // 2 - 50
                ball_1.y = HEIGHT // 2 - BALL_SIZE // 2
                ball_2.x = WIDTH // 2 - BALL_SIZE // 2 + 50
                ball_2.y = HEIGHT // 2 - BALL_SIZE // 2
                game_over = False
                message = ""
                show_restart_message = False
                continue

        screen.fill(BLACK)
        draw_score_and_lives()
        message_text = font_large.render(message, True, WHITE)
        screen.blit(message_text, (WIDTH // 2 - message_text.get_width() // 2, HEIGHT // 2 - 30))  # Ajustado la posición vertical

        if show_restart_message:
            restart_text = font_restart.render("[Presiona Enter para reiniciar el juego]", True, WHITE)
            screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 30))  # Ajustado la posición vertical

        pygame.display.flip()
        continue

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[K_w]:
        ball_1_dy = -BALL_SPEED
    elif keys[K_s]:
        ball_1_dy = BALL_SPEED
    else:
        ball_1_dy = 0
    if keys[K_UP]:
        ball_2_dy = -BALL_SPEED
    elif keys[K_DOWN]:
        ball_2_dy = BALL_SPEED
    else:
        ball_2_dy = 0

    ball_1.x += ball_1_dx
    ball_1.y += ball_1_dy
    ball_2.x += ball_2_dx
    ball_2.y += ball_2_dy

    paddle_left.y += paddle_left_dy
    paddle_right.y += paddle_right_dy

    if paddle_left.top <= 0 or paddle_left.bottom >= HEIGHT:
        paddle_left_dy = -paddle_left_dy
    if paddle_right.top <= 0 or paddle_right.bottom >= HEIGHT:
        paddle_right_dy = -paddle_right_dy

    if ball_1.colliderect(paddle_left) or ball_1.colliderect(paddle_right):
        ball_1_dx = -ball_1_dx
    if ball_2.colliderect(paddle_left) or ball_2.colliderect(paddle_right):
        ball_2_dx = -ball_2_dx

    if ball_1.x < 0 or ball_1.x > WIDTH:
        lives_1 -= 1
        ball_1.x = WIDTH // 2 - BALL_SIZE // 2 - 50
        ball_1.y = HEIGHT // 2 - BALL_SIZE // 2
        if ball_1.x > WIDTH:
            score_2 += 1
        else:
            score_1 += 1

    if ball_2.x < 0 or ball_2.x > WIDTH:
        lives_2 -= 1
        ball_2.x = WIDTH // 2 - BALL_SIZE // 2 + 50
        ball_2.y = HEIGHT // 2 - BALL_SIZE // 2
        if ball_2.x > WIDTH:
            score_1 += 1
        else:
            score_2 += 1

    if lives_1 <= 0 and lives_2 <= 0:
        message = "Es un empate"
        game_over = True
        show_restart_message = True
    elif lives_1 <= 0:
        message = "El jugador 2 ganó"
        game_over = True
        show_restart_message = True
    elif lives_2 <= 0:
        message = "El jugador 1 ganó"
        game_over = True
        show_restart_message = True

    # Añadir rebote en los bordes superior e inferior para ambas pelotas
    if ball_1.top <= 0:
        ball_1.top = 0  # Asegurarse de que no pase por encima
        ball_1_dy = -ball_1_dy
    if ball_2.top <= 0:
        ball_2.top = 0  # Asegurarse de que no pase por encima
        ball_2_dy = -ball_2_dy

    if ball_1.bottom >= HEIGHT:
        ball_1.bottom = HEIGHT  # Asegurarse de que no pase por debajo
        ball_1_dy = -ball_1_dy
    if ball_2.bottom >= HEIGHT:
        ball_2.bottom = HEIGHT  # Asegurarse de que no pase por debajo
        ball_2_dy = -ball_2_dy

    screen.fill(BLACK)
    pygame.draw.circle(screen, RED, ball_1.center, ball_1.width // 2)
    pygame.draw.circle(screen, BLUE, ball_2.center, ball_2.width // 2)
    pygame.draw.rect(screen, WHITE, paddle_left)
    pygame.draw.rect(screen, WHITE, paddle_right)

    draw_score_and_lives()
    pygame.display.flip()
    clock.tick(60)
