import socket
import pickle
import threading

# Server settings
HOST = 'localhost'
PORT = 4281

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

# Game parameters
paddle_width, paddle_height = 20, 150
width, height = 800, 600

clients = []
paddle_positions = [height // 2 - paddle_height // 2, height // 2 - paddle_height // 2]

# Ball parameters
ball_position = [width // 2, height // 2]
ball_speed = [3, 3]

lock = threading.Lock()

def handle_client(client, player_id):
    global clients, paddle_positions, ball_position, ball_speed

    try:
        while True:
            data = client.recv(1024)
            if not data:
                break

            paddle_positions[player_id] = pickle.loads(data)

            with lock:
                # Updating ball position (server decides movement)
                ball_position[0] += ball_speed[0]
                ball_position[1] += ball_speed[1]

                # Collision with top and bottom
                if ball_position[1] <= 0 or ball_position[1] >= height - 20:
                    ball_speed[1] = -ball_speed[1]

                # Collision with side walls (reset ball)
                if ball_position[0] <= 0 or ball_position[0] >= width:
                    ball_position = [width // 2, height // 2]
                    ball_speed = [5, 5]

                # Collision with paddles
                if (ball_position[0] <= 50 and paddle_positions[0] <= ball_position[1] <= paddle_positions[0] + paddle_height) or \
                   (ball_position[0] >= width - 50 and paddle_positions[1] <= ball_position[1] <= paddle_positions[1] + paddle_height):
                    ball_speed[0] = -ball_speed[0]

                # Creating data to send to each player
                data_to_send = {
                    "opponent_paddle": paddle_positions[1 - player_id],
                    "ball_position": [ball_position[0] if player_id == 0 else width - ball_position[0], ball_position[1]]
                }

            client.send(pickle.dumps(data_to_send))

    except:
        pass
    finally:
        clients.remove(client)
        client.close()

# Accepting two players
while len(clients) < 2:
    client, addr = server.accept()
    clients.append(client)
    player_id = len(clients) - 1

    client.send(pickle.dumps(player_id))

    thread = threading.Thread(target=handle_client, args=(client, player_id))
    thread.start()
