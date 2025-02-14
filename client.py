import socket
import pickle
import pygame
import sys

# Initialization of variables
HOST = 'localhost'
PORT = 4281
WHITE = (255, 255, 255)
width, height = 800, 600
paddle_width, paddle_height = 20, 150
ball_size = 20

# Initialize pygame
pygame.init()
win = pygame.display.set_mode((width, height))

# Creating paddles and ball
paddle = pygame.Rect(30, height // 2 - paddle_height // 2, paddle_width, paddle_height)
ball = pygame.Rect(width // 2 - ball_size // 2, height // 2 - ball_size // 2, ball_size, ball_size)

# Connecting to the server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

# Receiving player ID
player_id = pickle.loads(client.recv(1024))

# Opponent's paddle position
opponent_paddle = pygame.Rect(width - 50, height // 2 - paddle_height // 2, paddle_width, paddle_height)

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Handling player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and paddle.top > 0:
        paddle.y -= 5
    if keys[pygame.K_DOWN] and paddle.bottom < height:
        paddle.y += 5

    # Sending paddle position to the server
    client.send(pickle.dumps(paddle.y))

    # Receiving data from the server
    data = pickle.loads(client.recv(1024))
    opponent_paddle.y = data["opponent_paddle"]
    ball.x, ball.y = data["ball_position"]

    # Clearing the screen
    win.fill((0, 0, 0))

    # Drawing elements
    pygame.draw.rect(win, WHITE, paddle)
    pygame.draw.rect(win, WHITE, opponent_paddle)
    pygame.draw.ellipse(win, WHITE, ball)

    # Updating the screen
    pygame.display.flip()

    # Setting FPS
    clock.tick(60)
