import random

# Screen dimensions
WIDTH = 640
HEIGHT = 480

# Ball dimensions
BALL_SIZE = 20
BALL_SPEED = 5

# Paddle dimensions
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 60
PADDLE_SPEED = 5

class Rect:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

ball_1 = Rect(WIDTH // 2 - BALL_SIZE // 2 - 50, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)
ball_2 = Rect(WIDTH // 2 - BALL_SIZE // 2 + 50, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)
paddle_left = Rect(10, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
paddle_right = Rect(WIDTH - 20, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)

ball_1_dx = BALL_SPEED
ball_1_dy = 0
ball_2_dx = -BALL_SPEED
ball_2_dy = 0

score_1 = 0
score_2 = 0
lives_1 = 3
lives_2 = 3

game_over = False
message = ""
show_restart_message = False

def update_game_state(keys: list) -> dict:
    """
    Updates the game state based on the current key presses.

    Args:
        keys (list): A list of boolean values representing the state of keys.

    Returns:
        dict: A dictionary containing the updated positions of the balls and paddles,
              scores, lives, game over status, and messages.
    """
    global ball_1, ball_2, ball_1_dx, ball_1_dy, ball_2_dx, ball_2_dy, paddle_left, paddle_right, lives_1, lives_2, score_1, score_2, game_over, message, show_restart_message

    if keys[87]:  # W key
        paddle_left.y = max(0, paddle_left.y - PADDLE_SPEED)
    elif keys[83]:  # S key
        paddle_left.y = min(HEIGHT - PADDLE_HEIGHT, paddle_left.y + PADDLE_SPEED)
    
    if keys[38]:  # Up arrow
        paddle_right.y = max(0, paddle_right.y - PADDLE_SPEED)
    elif keys[40]:  # Down arrow
        paddle_right.y = min(HEIGHT - PADDLE_HEIGHT, paddle_right.y + PADDLE_SPEED)

    ball_1.x += ball_1_dx
    ball_1.y += ball_1_dy
    ball_2.x += ball_2_dx
    ball_2.y += ball_2_dy

    # Ball collisions with walls
    if ball_1.y <= 0 or ball_1.y + BALL_SIZE >= HEIGHT:
        ball_1_dy = -ball_1_dy
    if ball_2.y <= 0 or ball_2.y + BALL_SIZE >= HEIGHT:
        ball_2_dy = -ball_2_dy

    # Ball collisions with paddles
    if (ball_1.x <= paddle_left.x + PADDLE_WIDTH and ball_1.y + BALL_SIZE >= paddle_left.y and ball_1.y <= paddle_left.y + PADDLE_HEIGHT) or \
       (ball_1.x + BALL_SIZE >= paddle_right.x and ball_1.y + BALL_SIZE >= paddle_right.y and ball_1.y <= paddle_right.y + PADDLE_HEIGHT):
        ball_1_dx = -ball_1_dx

    if (ball_2.x <= paddle_left.x + PADDLE_WIDTH and ball_2.y + BALL_SIZE >= paddle_left.y and ball_2.y <= paddle_left.y + PADDLE_HEIGHT) or \
       (ball_2.x + BALL_SIZE >= paddle_right.x and ball_2.y + BALL_SIZE >= paddle_right.y and ball_2.y <= paddle_right.y + PADDLE_HEIGHT):
        ball_2_dx = -ball_2_dx

    # Scoring and resetting balls
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

    # Check for game over
    if lives_1 <= 0 and lives_2 <= 0:
        message = "It's a tie"
        game_over = True
        show_restart_message = True
    elif lives_1 <= 0:
        message = "Player 2 wins"
        game_over = True
        show_restart_message = True
    elif lives_2 <= 0:
        message = "Player 1 wins"
        game_over = True
        show_restart_message = True

    return {
        'ball_1': {'x': ball_1.x, 'y': ball_1.y},
        'ball_2': {'x': ball_2.x, 'y': ball_2.y},
        'paddle_left': {'y': paddle_left.y},
        'paddle_right': {'y': paddle_right.y},
        'score_1': score_1,
        'score_2': score_2,
        'lives_1': lives_1,
        'lives_2': lives_2,
        'game_over': game_over,
        'message': message,
        'show_restart_message': show_restart_message
    }

def reset_game() -> None:
    """
    Resets the game state to the initial conditions.

    This function resets the scores, lives, positions of the balls, and game over status.
    """
    global score_1, score_2, lives_1, lives_2, ball_1, ball_2, game_over, message, show_restart_message
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
