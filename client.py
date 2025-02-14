# Library initialization
import socket
import pickle
import pygame
import sys

# Initialize global variables
HOST = 'localhost'
PORT = 5555
WHITE = (255, 255, 255)  # color in RGB
width, height = 800, 600  # player screen size
paddle_width, paddle_height = 20, 100  # paddle size
ball_size = 20  # ball size

# Initialize the pygame module
pygame.init()

win = pygame.display.set_mode((width, height))  # display the game window

# Create the paddle object
paddle = pygame.Rect(width // 8 - paddle_width // 8, height // 8 - paddle_height // 8, paddle_width, paddle_height)

# Create the ball object
ball = pygame.Rect(width // 2 - ball_size // 2, height // 2 - ball_size // 2, ball_size, ball_size)
ball_speed = [5, 5]  # define ball movement speed

# Initialize the clock
clock = pygame.time.Clock()

# Create a client socket and connect to the server using the TCP protocol on localhost and the specified port (5555)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # AF_INET --> indicates the use of IPv4 addresses; SOCK_STREAM --> specifies the use of the TCP protocol, which provides a stream-based connection
client.connect((HOST, PORT))  # establish connection with the server

# Receive the player ID from the server
player_id = pickle.loads(client.recv(1024))

# Main game loop
while True:
    # Handle pygame events, e.g., closing the window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
    # Handle player paddle movement
    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP] and paddle.top > 0:
        paddle.y -= 5
    if keys[pygame.K_DOWN] and paddle.bottom < height:
        paddle.y += 5

    # Send the player's paddle position to the server
    client.send(pickle.dumps(paddle.y))

    # Receive the opponent's paddle position from the server
    opponent_paddle_y = pickle.loads(client.recv(1024))

    # Create a rectangle representing the opponent's paddle
    opponent_paddle = pygame.Rect(width - 50 - paddle_width, opponent_paddle_y, paddle_width, paddle_height)

    # Update ball position
    ball.x += ball_speed[0]
    ball.y += ball_speed[1]

    # Collision with paddles (ball bounce)
    if ball.colliderect(paddle) or ball.colliderect(opponent_paddle):
        ball_speed[0] = -ball_speed[0]

    # Collision with the top and bottom edges of the window (ball bounce)
    if ball.top <= 0 or ball.bottom >= height:
        ball_speed[1] = -ball_speed[1]

    # Ball goes out of the window area
    if ball.left <= 0 or ball.right >= width:
      
        ball.x = width // 2 - ball_size // 2
        ball.y = height // 2 - ball_size // 2
        
        ball_speed = [5, 5]

    # Clear the screen
    win.fill((0, 0, 0))

    # Draw paddles and ball
    pygame.draw.rect(win, WHITE, paddle)
    pygame.draw.rect(win, WHITE, opponent_paddle)
    pygame.draw.ellipse(win, WHITE, ball)

    # Update display
    pygame.display.flip()

    # Set frames per second
    clock.tick(60)
